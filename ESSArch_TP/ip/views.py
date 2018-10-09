"""
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
"""

import copy
import errno
import glob
import itertools
import logging
import os
import re
import shutil

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from groups_manager.utils import get_permission_name
from guardian.shortcuts import assign_perm
from natsort import natsorted
from rest_framework import exceptions, filters, permissions, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ESSArch_Core.WorkflowEngine.models import ProcessStep, ProcessTask
from ESSArch_Core.WorkflowEngine.serializers import ProcessStepChildrenSerializer
from ESSArch_Core.WorkflowEngine.util import create_workflow
from ESSArch_Core.auth.models import Group, Member
from ESSArch_Core.auth.serializers import ChangeOrganizationSerializer
from ESSArch_Core.auth.util import get_organization_groups
from ESSArch_Core.configuration.models import Path
from ESSArch_Core.exceptions import Conflict
from ESSArch_Core.filters import string_to_bool
from ESSArch_Core.ip.filters import InformationPackageFilter
from ESSArch_Core.ip.models import InformationPackage, EventIP
from ESSArch_Core.ip.permissions import CanChangeSA, CanCreateSIP, CanDeleteIP, CanSetUploaded, CanSubmitSIP, \
    CanUnlockProfile, CanUpload, IsResponsible
from ESSArch_Core.mixins import GetObjectForUpdateViewMixin
from ESSArch_Core.profiles.models import Profile, ProfileIP
from ESSArch_Core.util import find_destination, in_directory, mkdir_p, normalize_path
from ip.serializers import InformationPackageSerializer, InformationPackageReadSerializer


class InformationPackageViewSet(viewsets.ModelViewSet, GetObjectForUpdateViewMixin):
    """
    API endpoint that allows information packages to be viewed or edited.
    """
    logger = logging.getLogger('essarch.etp.InformationPackageViewSet')
    queryset = InformationPackage.objects.none()
    serializer_class = InformationPackageSerializer
    filter_backends = (
        filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter,
    )
    ordering_fields = (
        'label', 'responsible', 'create_date', 'state',
        'id', 'object_identifier_value',
    )
    search_fields = (
        'object_identifier_value', 'label', 'responsible__first_name',
        'responsible__last_name', 'responsible__username', 'state',
        'submission_agreement__name', 'start_date', 'end_date',
    )
    filter_class = InformationPackageFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return InformationPackageReadSerializer

        return InformationPackageSerializer

    def get_permissions(self):
        if self.action in ['partial_update', 'update']:
            if self.request.data.get('submission_agreement'):
                self.permission_classes = [CanChangeSA]
        if self.action == 'destroy':
            self.permission_classes = [CanDeleteIP]

        return super(InformationPackageViewSet, self).get_permissions()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        lookup_field = self.lookup_field

        objid = self.request.query_params.get('objid')
        if objid is not None:
            lookup_field = 'object_identifier_value'

        filter_kwargs = {lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        user = self.request.user
        queryset = InformationPackage.objects.visible_to_user(user)
        queryset = queryset.prefetch_related(
            Prefetch('profileip_set', to_attr='profiles'), 'profiles__profile', 'agents',
            'responsible__user_permissions', 'responsible__groups__permissions', 'steps',
        ).select_related('submission_agreement')
        return queryset

    @detail_route(methods=['post'], url_path='change-organization')
    def change_organization(self, request, pk=None):
        ip = self.get_object()

        serializer = ChangeOrganizationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        org = serializer.validated_data['organization']

        ip.change_organization(org)
        return Response()

    def create(self, request, *args, **kwargs):
        """
        Prepares a new information package (IP) using the following tasks:

        1. Creates a new IP in the database.

        2. Creates a directory in the prepare directory with the name set to
        the id of the new IP.

        3. Creates an event in the database connected to the IP and with the
        detail "Prepare IP".

        Args:

        Returns:
            None
        """

        self.check_permissions(request)

        try:
            label = request.data['label']
        except KeyError:
            raise exceptions.ParseError('Missing parameter label')

        object_identifier_value = request.data.get('object_identifier_value')
        responsible = self.request.user

        if responsible.user_profile.current_organization is None:
            raise exceptions.ParseError('You must be part of an organization to prepare an IP')

        prepare_path = Path.objects.get(entity="path_preingest_prepare").value
        if object_identifier_value:
            ip_exists = InformationPackage.objects.filter(object_identifier_value=object_identifier_value).exists()
            if ip_exists:
                raise Conflict('IP with object identifer value "%s" already exists' % object_identifier_value)

            if os.path.exists(os.path.join(prepare_path, object_identifier_value)):
                raise Conflict('IP with identifier "%s" already exists on disk' % object_identifier_value)

        perms = copy.deepcopy(getattr(settings, 'IP_CREATION_PERMS_MAP', {}))
        try:
            with transaction.atomic():
                ip = InformationPackage.objects.create(object_identifier_value=object_identifier_value, label=label,
                                                       responsible=responsible, state="Preparing",
                                                       package_type=InformationPackage.SIP)
                ip.entry_date = ip.create_date
                extra = {'event_type': 10100, 'object': str(ip.pk), 'agent': request.user.username, 'outcome': EventIP.SUCCESS}
                self.logger.info("Prepared {obj}".format(obj=ip.object_identifier_value), extra=extra)

                member = Member.objects.get(django_user=responsible)
                user_perms = perms.pop('owner', [])
                organization = member.django_user.user_profile.current_organization
                organization.assign_object(ip, custom_permissions=perms)
                organization.add_object(ip)

                for perm in user_perms:
                    perm_name = get_permission_name(perm, ip)
                    assign_perm(perm_name, member.django_user, ip)

                obj_path = normalize_path(os.path.join(prepare_path, ip.object_identifier_value))
                os.mkdir(obj_path)
                ip.object_path = obj_path
                ip.save()
                extra = {'event_type': 10200, 'object': str(ip.pk), 'agent': request.user.username, 'outcome': EventIP.SUCCESS}
                self.logger.info("Created IP root directory", extra=extra)
        except IntegrityError:
            try:
                shutil.rmtree(obj_path)
            except OSError as e:
                pass
            raise

        return Response({"detail": "Prepared IP"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        ip = self.get_object()

        if 'submission_agreement' in request.data:
            if ip.submission_agreement_locked:
                return Response("SA connected to IP is locked", status=status.HTTP_400_BAD_REQUEST)

        return super(InformationPackageViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        ip = self.get_object()
        path = ip.object_path

        if os.path.isdir(path):
            t = ProcessTask.objects.create(
                name='ESSArch_Core.tasks.DeleteFiles',
                params={'path': path},
                eager=False,
                responsible=request.user,
            )
            t.run()
        else:
            no_ext = os.path.splitext(path)[0]
            step = ProcessStep.objects.create(
                name="Delete files",
                eager=False,
            )

            for fl in [no_ext + '.' + ext for ext in ['xml', 'tar', 'zip']]:
                t = ProcessTask.objects.create(
                    name='ESSArch_Core.tasks.DeleteFiles',
                    params={'path': fl},
                    processstep=step,
                    responsible=request.user,
                )
                t.run()

            step.run()

        return super(InformationPackageViewSet, self).destroy(request, *args, **kwargs)

    @detail_route()
    def workflow(self, request, pk=None):
        ip = self.get_object()
        hidden = request.query_params.get('hidden')

        steps = ip.steps.filter(parent_step__information_package__isnull=True)
        tasks = ip.processtask_set.filter(processstep__information_package__isnull=True)

        if hidden is not None:
            steps = steps.filter(hidden=string_to_bool(hidden))
            tasks = tasks.filter(hidden=string_to_bool(hidden))

        flow = sorted(itertools.chain(steps, tasks), key=lambda x: (x.get_pos(), x.time_created))

        serializer = ProcessStepChildrenSerializer(data=flow, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)

    @detail_route(methods=['delete', 'get', 'post'], permission_classes=[IsResponsible])
    def files(self, request, pk=None):
        ip = self.get_object()

        if request.method not in permissions.SAFE_METHODS:
            if ip.state not in ['Prepared', 'Uploading']:
                raise exceptions.ParseError("Cannot delete or add content of an IP that is not in 'Prepared' or 'Uploading' state")

        if request.method == 'DELETE':
            try:
                path = request.data['path']
            except KeyError:
                return Response('Path parameter missing', status=status.HTTP_400_BAD_REQUEST)

            root = ip.object_path
            fullpath = os.path.join(root, path)

            if not in_directory(fullpath, root):
                raise exceptions.ParseError('Illegal path %s' % path)

            try:
                shutil.rmtree(fullpath)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    raise exceptions.NotFound('Path does not exist')

                if e.errno != errno.ENOTDIR:
                    raise

                os.remove(fullpath)

            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == 'POST':
            try:
                path = request.data['path']
            except KeyError:
                return Response('Path parameter missing', status=status.HTTP_400_BAD_REQUEST)

            try:
                pathtype = request.data['type']
            except KeyError:
                return Response('Type parameter missing', status=status.HTTP_400_BAD_REQUEST)

            root = ip.object_path
            fullpath = os.path.join(root, path)

            if not in_directory(fullpath, root):
                raise exceptions.ParseError('Illegal path %s' % path)

            if pathtype == 'dir':
                try:
                    os.makedirs(fullpath)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        raise exceptions.ParseError('Directory %s already exists' % path)

                    raise

            elif pathtype == 'file':
                open(fullpath, 'a').close()
            else:
                return Response('Type must be either "file" or "dir"', status=status.HTTP_400_BAD_REQUEST)

            return Response(path, status=status.HTTP_201_CREATED)

        path = request.query_params.get('path', '').rstrip('/')
        download = request.query_params.get('download', False)
        return ip.get_path_response(path, request, force_download=download, paginator=self.paginator)

    @detail_route(methods=['get', 'post'], url_path='ead-editor')
    def ead_editor(self, request, pk=None):
        ip = self.get_object()
        try:
            structure = ip.get_profile('sip').structure
        except AttributeError:
            return Response("No SIP profile for IP created yet", status=status.HTTP_400_BAD_REQUEST)

        ead_dir, ead_name = find_destination("archival_description_file", structure)

        if ead_name is None:
            return Response("No EAD file for IP found", status=status.HTTP_404_NOT_FOUND)

        xmlfile = os.path.join(ip.object_path, ead_dir, ead_name)

        if request.method == 'GET':

            try:
                with open(xmlfile) as f:
                    s = f.read()
                    return Response({"data": s})
            except IOError:
                open(xmlfile, 'a').close()
                return Response({"data": ""})

        content = request.POST.get("content", '')

        with open(xmlfile, "w") as f:
            f.write(str(content))
            return Response("Content written to %s" % xmlfile)

    @list_route(methods=['get'], url_path='get-xsds')
    def get_xsds(self, request, pk=None):
        static_path = os.path.join(settings.BASE_DIR, 'static/edead/xsds')
        filename_list = os.listdir(static_path)
        return Response(filename_list)

    @transaction.atomic
    @detail_route(methods=['post'], url_path='prepare')
    def prepare(self, request, pk=None):
        ip = self.get_object_for_update()
        if ip.is_locked():
            raise Conflict('Information package is locked')
        sa = ip.submission_agreement

        if ip.state != 'Preparing':
            raise exceptions.ParseError('IP must be in state "Preparing"')

        if sa is None or not ip.submission_agreement_locked:
            raise exceptions.ParseError('IP requires locked SA to be prepared')

        profile_ip_sip = ProfileIP.objects.filter(ip=ip, profile=sa.profile_sip).first()
        profile_ip_transfer_project = ProfileIP.objects.filter(ip=ip, profile=sa.profile_transfer_project).first()
        profile_ip_submit_description = ProfileIP.objects.filter(ip=ip, profile=sa.profile_submit_description).first()

        if profile_ip_sip is None:
            raise exceptions.ParseError('Information package missing SIP profile')
        if profile_ip_transfer_project is None:
            raise exceptions.ParseError('Information package missing Transfer Project profile')
        if profile_ip_submit_description is None:
            raise exceptions.ParseError('Information package missing Submit Description profile')

        for profile_ip in ProfileIP.objects.filter(ip=ip).iterator():
            try:
                profile_ip.clean()
            except ValidationError as e:
                raise exceptions.ParseError('%s: %s' % (profile_ip.profile.name, e[0]))

            profile_ip.LockedBy = request.user
            profile_ip.save()

        step = ProcessStep.objects.create(
            name="Create Physical Model",
            information_package=ip
        )
        ProcessTask.objects.create(
            name="ESSArch_Core.ip.tasks.CreatePhysicalModel",
            information_package=ip,
            responsible=self.request.user,
            processstep=step,
        )

        step.run().get()

        submit_description_data = ip.get_profile_data('submit_description')
        ip.start_date = submit_description_data.get('start_date')
        ip.end_date = submit_description_data.get('end_date')

        ip.state = "Prepared"
        ip.save(update_fields=['state', 'start_date', 'end_date'])

        return Response()

    @transaction.atomic
    @detail_route(methods=['post'], url_path='create', permission_classes=[CanCreateSIP])
    def create_ip(self, request, pk=None):
        """
        Creates the specified information package

        Args:
            pk: The primary key (id) of the information package to create

        Returns:
            None
        """

        ip = self.get_object_for_update()
        if ip.is_locked():
            raise Conflict('Information package is locked')

        if ip.state != "Uploaded":
            raise exceptions.ParseError("The IP (%s) is in the state '%s' but should be 'Uploaded'" % (pk, ip.state))

        ip.state = 'Creating'
        ip.save()

        generate_premis = ip.profile_locked('preservation_metadata')

        convert_files = request.data.get('file_conversion', False)
        file_format_map = {
            'doc': 'pdf',
            'docx': 'pdf'
        }

        validators = request.data.get('validators', {})
        validate_xml_file = validators.get('validate_xml_file', False)
        validate_logical_physical_representation = validators.get('validate_logical_physical_representation', False)

        workflow_spec = [
            {
                "name": "ESSArch_Core.tasks.ConvertFile",
                "if": convert_files,
                "label": "Convert Files",
                "args": ["{{_OBJPATH}}", file_format_map]
            },
            {
                "name": "ESSArch_Core.ip.tasks.DownloadSchemas",
                "label": "Download Schemas",
            },
            {
                "step": True,
                "name": "Create Log File",
                "children": [
                    {
                        "name": "ESSArch_Core.ip.tasks.GenerateEventsXML",
                        "label": "Generate events xml file",
                    },
                    {
                        "name": "ESSArch_Core.tasks.AppendEvents",
                        "label": "Add events to xml file",
                    },
                    {
                        "name": "ESSArch_Core.ip.tasks.AddPremisIPObjectElementToEventsFile",
                        "label": "Add premis IP object to xml file",
                    },

                ]
            },
            {
                "name": "ESSArch_Core.ip.tasks.GeneratePremis",
                "if": generate_premis,
                "label": "Generate premis",
            },
            {
                "name": "ESSArch_Core.ip.tasks.GenerateContentMets",
                "label": "Generate content-mets",
            },
            {
                "step": True,
                "name": "Validation",
                "if": any([validate_xml_file, validate_logical_physical_representation]),
                "children": [
                    {
                        "name": "ESSArch_Core.tasks.ValidateXMLFile",
                        "if": validate_xml_file,
                        "label": "Validate content-mets",
                        "params": {
                            "xml_filename": "{{_CONTENT_METS_PATH}}",
                        }
                    },
                    {
                        "name": "ESSArch_Core.tasks.ValidateXMLFile",
                        "if": generate_premis and validate_xml_file,
                        "label": "Validate premis",
                        "params": {
                            "xml_filename": "{{_PREMIS_PATH}}",
                        }
                    },
                    {
                        "name": "ESSArch_Core.tasks.ValidateLogicalPhysicalRepresentation",
                        "if": validate_logical_physical_representation,
                        "label": "Diff-check against content-mets",
                        "args": ["{{_OBJPATH}}", "{{_CONTENT_METS_PATH}}"],
                    },
                    {
                        "name": "ESSArch_Core.tasks.CompareXMLFiles",
                        "if": generate_premis,
                        "label": "Compare premis and content-mets",
                        "args": ["{{_PREMIS_PATH}}", "{{_CONTENT_METS_PATH}}"],
                    }
                ]
            },
            {
                "name": "ESSArch_Core.ip.tasks.CreateContainer",
                "label": "Create container",
            },
            {
                "name": "ESSArch_Core.tasks.UpdateIPStatus",
                "label": "Set status to created",
                "args": ["Created"],
            },
        ]
        workflow = create_workflow(workflow_spec, ip)
        workflow.name = "Create SIP"
        workflow.information_package = ip
        workflow.save()
        workflow.run()
        return Response({'status': 'creating ip'})

    @transaction.atomic
    @detail_route(methods=['post'], url_path='submit', permission_classes=[CanSubmitSIP])
    def submit(self, request, pk=None):
        """
        Submits the specified information package

        Args:
            pk: The primary key (id) of the information package to submit

        Returns:
            None
        """

        ip = self.get_object_for_update()
        if ip.is_locked():
            raise Conflict('Information package is locked')

        if ip.state != "Created":
            return Response(
                "The IP (%s) is in the state '%s' but should be 'Created'" % (pk, ip.state),
                status=status.HTTP_400_BAD_REQUEST
            )

        ip.state = 'Submitting'
        ip.save()

        sd_profile = ip.get_profile('submit_description')

        if sd_profile is None:
            return Response(
                "The IP (%s) has no submit description profile" % pk,
                status=status.HTTP_400_BAD_REQUEST
            )

        email_subject = None
        email_body = None
        recipient = ip.get_email_recipient()
        if recipient:
            for arg in ['subject', 'body']:
                if arg not in request.data:
                    raise exceptions.ParseError('%s parameter missing' % arg)

            email_subject = request.data['subject']
            email_body = request.data['body']

        validators = request.data.get('validators', {})
        validate_xml_file = validators.get('validate_xml_file', False)
        validate_logical_physical_representation = validators.get('validate_logical_physical_representation', False)

        workflow_spec = [
            {
                "name": "ESSArch_Core.ip.tasks.GeneratePackageMets",
                "label": "Generate package-mets",
            },
            {
                "name": "ESSArch_Core.tasks.ValidateXMLFile",
                "if": validate_xml_file,
                "label": "Validate package-mets",
                "params": {
                    "xml_filename": "{{_PACKAGE_METS_PATH}}",
                }
            },
            {
                "name": "ESSArch_Core.tasks.ValidateLogicalPhysicalRepresentation",
                "if": validate_logical_physical_representation,
                "label": "Diff-check against package-mets",
                "args": ["{{_OBJPATH}}", "{{_PACKAGE_METS_PATH}}"],
            },
            {
                "name": "preingest.tasks.SubmitSIP",
                "label": "Submit SIP",
            },
            {
                "name": "ESSArch_Core.tasks.UpdateIPStatus",
                "label": "Set status to submitted",
                "args": ["Submitted"],
            },
            {
                "name": "ESSArch_Core.tasks.SendEmail",
                "if": recipient,
                "label": "Send email",
                "params": {
                    "subject": email_subject,
                    "body": email_body,
                    "recipients": [recipient],
                    "attachments": [
                        "{{_PACKAGE_METS_PATH}}",
                    ],
                }
            },
        ]
        workflow = create_workflow(workflow_spec, ip)
        workflow.name = "Submit SIP"
        workflow.information_package = ip
        workflow.save()
        workflow.run()
        return Response({'status': 'submitting ip'})

    @detail_route(methods=['put'], url_path='check-profile')
    def check_profile(self, request, pk=None):
        ip = self.get_object()
        ptype = request.data.get("type")
        pip = ProfileIP.objects.get(ip=ip, profile__profile_type=ptype)

        if not pip.LockedBy:
            pip.included = request.data.get('checked', not pip.included)
            pip.save()

        return Response()

    @detail_route(methods=['put'], url_path='change-profile')
    def change_profile(self, request, pk=None):
        ip = self.get_object()
        new_profile = Profile.objects.get(pk=request.data["new_profile"])

        try:
            ip.change_profile(new_profile)
        except ValueError as e:
            return Response({'status': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 'updating IP (%s) with new profile (%s)' % (
                ip, new_profile
            )
        })

    @detail_route(methods=['post'], url_path='unlock-profile', permission_classes=[CanUnlockProfile])
    def unlock_profile(self, request, pk=None):
        ip = self.get_object()

        if ip.state in ['Submitting', 'Submitted']:
            raise exceptions.ParseError('Cannot unlock profiles in an IP that is %s' % ip.state)

        try:
            ptype = request.data["type"]
        except KeyError:
            raise exceptions.ParseError('type parameter missing')

        ip.unlock_profile(ptype)
        prepare_path = Path.objects.get(entity='path_preingest_prepare').value
        ip.object_path = normalize_path(os.path.join(prepare_path, ip.object_identifier_value))
        ip.save(update_fields=['object_path'])

        return Response({
            'status': 'unlocking profile with type "%s" in IP "%s"' % (
                ptype, ip.pk
            )
        })

    @detail_route(methods=['get', 'post'], url_path='upload', permission_classes=[CanUpload])
    def upload(self, request, pk=None):
        ip = self.get_object()
        if ip.state not in ['Prepared', 'Uploading']:
            raise exceptions.ParseError('IP must be in state "Prepared" or "Uploading"')

        ip.state = "Uploading"
        ip.save()

        if request.method == 'GET':
            dst = request.GET.get('destination', '').strip('/ ')
            path = os.path.join(dst, request.GET.get('flowRelativePath', ''))
            chunk_nr = request.GET.get('flowChunkNumber')
            chunk_path = "%s_%s" % (path, chunk_nr)

            if os.path.exists(os.path.join(ip.object_path, chunk_path)):
                return HttpResponse(status=200)
            return HttpResponse(status=204)

        if request.method == 'POST':
            dst = request.data.get('destination', '').strip('/ ')
            path = os.path.join(dst, request.data.get('flowRelativePath', ''))
            chunk_nr = request.data.get('flowChunkNumber')
            chunk_path = "%s_%s" % (path, chunk_nr)
            chunk_path = os.path.join(ip.object_path, chunk_path)

            chunk = request.FILES['file']

            if not os.path.exists(os.path.dirname(chunk_path)):
                mkdir_p(os.path.dirname(chunk_path))

            with open(chunk_path, 'wb+') as dst:
                for c in chunk.chunks():
                    dst.write(c)

            return Response("Uploaded chunk")

    @detail_route(methods=['post'], url_path='merge-uploaded-chunks', permission_classes=[CanUpload])
    def merge_uploaded_chunks(self, request, pk=None):
        ip = self.get_object()
        if ip.state != 'Uploading':
            raise exceptions.ParseError('IP must be in state "Uploading"')

        path = os.path.join(ip.object_path, request.data['path'])

        with open(path, 'wb') as f:
            for chunk_file in natsorted(glob.glob('%s_*' % re.sub(r'([\[\]])', '[\\1]', path))):
                with open(chunk_file, 'rb') as cf:
                    f.write(cf.read())
                cf.close()
                os.remove(chunk_file)

        logger = logging.getLogger('essarch')
        extra = {'event_type': 50700, 'object': str(ip.pk), 'agent': request.user.username, 'outcome': EventIP.SUCCESS}
        logger.info("Uploaded %s" % path, extra=extra)

        return Response("Merged chunks")

    @detail_route(methods=['post'], url_path='set-uploaded', permission_classes=[CanSetUploaded])
    def set_uploaded(self, request, pk=None):
        ip = self.get_object()
        if ip.state not in ['Prepared', 'Uploading']:
            raise exceptions.ParseError('IP must be in state "Prepared" or "Uploading"')

        ProcessTask.objects.create(
            name="ESSArch_Core.tasks.UpdateIPSizeAndCount",
            eager=False,
            information_package=ip
        ).run()

        ip.state = "Uploaded"
        ip.save()
        return Response()
