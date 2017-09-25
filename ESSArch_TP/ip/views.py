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

from _version import get_versions

from collections import OrderedDict

import errno
import glob
import os
import shutil
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Prefetch
from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import exceptions, filters, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response

from natsort import natsorted

from scandir import walk

from ESSArch_Core.exceptions import Conflict

from ESSArch_Core.configuration.models import (
    EventType,
    Path,
)

from ESSArch_Core.ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
    InformationPackage,
    EventIP
)

from ESSArch_Core.ip.permissions import (
    CanChangeSA,
    CanCreateSIP,
    CanDeleteIP,
    CanSetUploaded,
    CanSubmitSIP,
    CanUnlockProfile,
    CanUpload,
    IsResponsible,
)

from ESSArch_Core.ip.serializers import EventIPSerializer

from ESSArch_Core.profiles.models import (
    Profile,
    ProfileIP,
    ProfileIPData,
)

from ESSArch_Core.profiles.utils import fill_specification_data

from ESSArch_Core.util import (
    create_event,
    creation_date,
    find_destination,
    get_event_spec,
    get_files_and_dirs,
    get_tree_size_and_count,
    in_directory,
    mkdir_p,
    timestamp_to_datetime,
)

from ESSArch_Core.WorkflowEngine.models import (
    ProcessStep, ProcessTask,
)

from ip.filters import (
    ArchivalInstitutionFilter,
    ArchivistOrganizationFilter,
    ArchivalTypeFilter,
    ArchivalLocationFilter,
    InformationPackageFilter,
)

from ip.serializers import (
    ArchivalInstitutionSerializer,
    ArchivistOrganizationSerializer,
    ArchivalTypeSerializer,
    ArchivalLocationSerializer,
    InformationPackageSerializer,
)

from ESSArch_Core.WorkflowEngine.serializers import (
    ProcessStepSerializer,
)

from ip.steps import (
    prepare_ip,
)

from rest_framework import viewsets


class ArchivalInstitutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archival institutions to be viewed or edited.
    """
    queryset = ArchivalInstitution.objects.all()
    serializer_class = ArchivalInstitutionSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = ArchivalInstitutionFilter


class ArchivistOrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archivist organizations to be viewed or edited.
    """
    queryset = ArchivistOrganization.objects.all()
    serializer_class = ArchivistOrganizationSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = ArchivistOrganizationFilter


class ArchivalTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archival types to be viewed or edited.
    """
    queryset = ArchivalType.objects.all()
    serializer_class = ArchivalTypeSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = ArchivalTypeFilter


class ArchivalLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archival locations to be viewed or edited.
    """
    queryset = ArchivalLocation.objects.all()
    serializer_class = ArchivalLocationSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = ArchivalLocationFilter


class InformationPackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows information packages to be viewed or edited.
    """
    queryset = InformationPackage.objects.all().prefetch_related(
        Prefetch('profileip_set', to_attr='profiles'), 'profiles__profile',
        'archival_institution', 'archivist_organization', 'archival_type', 'archival_location',
        'responsible__user_permissions', 'responsible__groups__permissions', 'steps',
    ).select_related('submission_agreement')
    serializer_class = InformationPackageSerializer
    filter_backends = (
        filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter,
    )
    ordering_fields = (
        'label', 'responsible', 'create_date', 'state', 'eventDateTime',
        'eventType', 'eventOutcomeDetailNote', 'eventOutcome',
        'linkingAgentIdentifierValue', 'id', 'object_identifier_value',
    )
    search_fields = (
        'object_identifier_value', 'label', 'responsible__first_name',
        'responsible__last_name', 'responsible__username', 'state',
        'submission_agreement__name', 'start_date', 'end_date',
    )
    filter_class = InformationPackageFilter

    def get_permissions(self):
        if self.action in ['partial_update', 'update']:
            if self.request.data.get('submission_agreement'):
                self.permission_classes = [CanChangeSA]
        if self.action == 'destroy':
            self.permission_classes = [CanDeleteIP]

        return super(InformationPackageViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = self.queryset

        other = self.request.query_params.get('other')

        if other is not None:
            queryset = queryset.filter(
                archival_institution=None,
                archivist_organization=None,
                archival_type=None,
                archival_location=None
            )

        return queryset

    def create(self, request):
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

        if object_identifier_value:
            ip_exists = InformationPackage.objects.filter(object_identifier_value=object_identifier_value).exists()
            if ip_exists:
                raise Conflict('IP with object identifer value "%s" already exists' % object_identifier_value)

            prepare_path = Path.objects.get(entity="path_preingest_prepare").value

            if os.path.exists(os.path.join(prepare_path, object_identifier_value)):
                raise Conflict('IP with identifier "%s" already exists on disk' % object_identifier_value)

        prepare_ip(label, responsible, object_identifier_value).run()
        return Response({"detail": "Prepared IP"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        ip = self.get_object()

        if 'submission_agreement' in request.data:
            if ip.submission_agreement_locked:
                return Response("SA connected to IP is locked", status=status.HTTP_400_BAD_REQUEST)

        return super(InformationPackageViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        ip = self.get_object()
        self.check_object_permissions(request, ip)
        path = ip.object_path

        try:
            shutil.rmtree(path)
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                no_ext = os.path.splitext(path)[0]

                for fl in glob.glob(no_ext + "*"):
                    try:
                        os.remove(fl)
                    except:
                        raise
            elif e.errno == errno.ENOENT:
                pass
            else:
                raise

        try:
            shutil.rmtree(ip.object_path)
        except:
            pass

        try:
            os.remove(ip.object_path + ".tar")
        except:
            pass

        try:
            os.remove(ip.object_path + ".zip")
        except:
            pass

        return super(InformationPackageViewSet, self).destroy(request, pk=pk)

    @detail_route()
    def events(self, request, pk=None):
        ip = self.get_object()
        events = filters.OrderingFilter().filter_queryset(request, EventIP.objects.filter(linkingObjectIdentifierValue=ip.object_identifier_value), self)
        page = self.paginate_queryset(events)
        if page is not None:
            serializers = EventIPSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializers.data)
        serializers = EventIPSerializer(events, many=True, context={'request': request})
        return Response(serializers.data)

    @detail_route()
    def steps(self, request, pk=None):
        ip = self.get_object()
        steps = ip.steps.all()
        serializer = ProcessStepSerializer(
            data=steps, many=True, context={'request': request}
        )
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

        return ip.files(request.query_params.get('path', '').rstrip('/'))

    @detail_route(methods=['get', 'post'], url_path='ead-editor')
    def ead_editor(self, request, pk=None):
        ip = self.get_object()
        try:
            structure = ip.get_profile('sip').structure
        except AttributeError:
            return Response("No SIP profile for IP created yet", status=status.HTTP_400_BAD_REQUEST)

        ead_dir, ead_name = find_destination("archival_description_file", structure)

        if ead_name is None:
            return Response("No EAD file for IP found", status=status.HTTP_404_BAD_REQUEST)

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

    @detail_route(methods=['post'], url_path='prepare')
    def prepare(self, request, pk=None):
        ip = self.get_object()
        sa = ip.submission_agreement

        if sa is None or not ip.submission_agreement_locked:
            raise exceptions.ParseError('IP requires locked SA to be prepared')

        for profile_ip in ProfileIP.objects.filter(ip=ip).iterator():
            try:
                profile_ip.clean()
            except ValidationError as e:
                raise exceptions.ParseError('%s: %s' % (profile_ip.profile.name, e[0]))

            if profile_ip.data is None:
                if profile_ip.data_versions.count():
                    profile_ip.data = profile_ip.data_versions.last()
                else:
                    data = {}
                    for field in profile_ip.profile.template:
                        try:
                            data[field['key']] = field['defaultValue']
                        except KeyError:
                            pass
                    data_obj = ProfileIPData.objects.create(
                        relation=profile_ip, data=data, version=0, user=request.user,
                    )
                    profile_ip.data = data_obj

            profile_ip.LockedBy = request.user
            profile_ip.save()

        profile_ip_sip = ProfileIP.objects.filter(ip=ip, profile=sa.profile_sip).first()
        profile_ip_transfer_project = ProfileIP.objects.filter(ip=ip, profile=sa.profile_transfer_project).first()
        profile_ip_submit_description = ProfileIP.objects.filter(ip=ip, profile=sa.profile_submit_description).first()

        if profile_ip_sip is None:
            raise exceptions.ParseError('Information package missing SIP profile')

        if profile_ip_transfer_project is None:
            raise exceptions.ParseError('Information package missing Transfer Project profile')

        if profile_ip_submit_description is None:
            raise exceptions.ParseError('Information package missing Submit Description profile')

        root = os.path.join(
            Path.objects.get(
                entity="path_preingest_prepare"
            ).value,
            ip.object_identifier_value
        )

        step = ProcessStep.objects.create(
            name="Create Physical Model",
            information_package=ip
        )
        ProcessTask.objects.create(
            name="preingest.tasks.CreatePhysicalModel",
            params={
                "structure": sa.profile_sip.structure,
                "root": root
            },
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
            processstep=step,
        )

        step.run().get()

        transfer_project = sa.profile_transfer_project
        transfer_project_data = ProfileIP.objects.get(profile=transfer_project, ip=ip).data.data

        archival_institution = transfer_project_data.get("archival_institution")
        archival_type = transfer_project_data.get("archival_type")
        archival_location = transfer_project_data.get("archival_location")

        if archival_institution is not None:
            try:
                (arch, _) = ArchivalInstitution.objects.get_or_create(
                    name=archival_institution
                )
            except IntegrityError:
                arch = ArchivalInstitution.objects.get(
                    name=archival_institution
                )
            ip.archival_institution = arch

        if archival_type is not None:
            try:
                (arch, _) = ArchivalType.objects.get_or_create(
                    name=archival_type
                )
            except IntegrityError:
                arch = ArchivalType.objects.get(
                    name=archival_type
                )
            ip.archival_type = arch

        if archival_location is not None:
            try:
                (arch, _) = ArchivalLocation.objects.get_or_create(
                    name=archival_location
                )
            except IntegrityError:
                arch = ArchivalLocation.objects.get(
                    name=archival_location
                )
            ip.archival_location = arch

        ip.state = "Prepared"
        ip.save(update_fields=['archival_institution', 'archival_type', 'archival_location', 'state'])

        return Response()

    @detail_route(methods=['post'], url_path='create', permission_classes=[CanCreateSIP])
    def create_ip(self, request, pk=None):
        """
        Creates the specified information package

        Args:
            pk: The primary key (id) of the information package to create

        Returns:
            None
        """

        ip = self.get_object()
        sa = ip.submission_agreement
        agent = request.user

        if ip.state != "Uploaded":
            raise ValueError(
                "The IP (%s) is in the state '%s' but should be 'Uploaded'" % (pk, ip.state)
            )

        validators = request.data.get('validators', {})

        validate_xml_file = validators.get('validate_xml_file', False)
        validate_file_format = validators.get('validate_file_format', False)
        validate_integrity = validators.get('validate_integrity', False)
        validate_logical_physical_representation = validators.get('validate_logical_physical_representation', False)

        file_conversion = request.data.get('file_conversion', False)

        container_format = ip.get_container_format()

        main_step = ProcessStep.objects.create(
            name="Create SIP",
            eager=False,
        )

        t0 = ProcessTask.objects.create(
            name="ESSArch_Core.tasks.UpdateIPStatus",
            params={
                "ip": ip.pk,
                "status": "Creating",
            },
            processstep_pos=0,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        )
        start_create_sip_step = ProcessStep.objects.create(
            name="Update IP Status",
            parent_step_pos=0
        )

        start_create_sip_step.add_tasks(t0)

        event_type = EventType.objects.get(eventType=10200)

        create_event(event_type, 0, "Created SIP", get_versions()['version'], agent, ip=ip)

        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        reception_path = Path.objects.get(
            entity="path_preingest_reception"
        ).value

        ip_prepare_path = os.path.join(prepare_path, ip.object_identifier_value)
        ip_reception_path = os.path.join(reception_path, ip.object_identifier_value)
        events_path = os.path.join(ip_prepare_path, "ipevents.xml")

        profile_ip_sip = ip.get_profile_rel('sip')
        structure = profile_ip_sip.profile.structure
        info = fill_specification_data(profile_ip_sip.data.data, ip=ip, sa=sa)

        # ensure premis is created before mets
        filesToCreate = OrderedDict()

        if ip.profile_locked('preservation_metadata'):
            premis_profile = ip.get_profile('preservation_metadata')
            premis_dir, premis_name = find_destination("preservation_description_file", structure)
            premis_path = os.path.join(ip.object_path, premis_dir, premis_name)
            filesToCreate[premis_path] = premis_profile.specification

        mets_dir, mets_name = find_destination("mets_file", structure)
        mets_path = os.path.join(ip.object_path, mets_dir, mets_name)
        filesToCreate[mets_path] = profile_ip_sip.profile.specification

        if file_conversion:
            convert_files_step = ProcessStep.objects.create(
                name="Convert files",
                parent_step_pos=10,
                parallel=False,
            )

            FILE_FORMAT_MAP = {
                'doc': 'pdf',
                'docx': 'pdf'
            }

            tasks = []

            for root, dirs, filenames in walk(ip.object_path):
                for fname in filenames:
                    filepath = os.path.join(root, fname)
                    try:
                        new_format = FILE_FORMAT_MAP[os.path.splitext(filepath)[1][1:]]
                    except KeyError:
                        pass
                    else:
                        tasks.append(ProcessTask(
                            name="ESSArch_Core.tasks.ConvertFile",
                            params={
                                'filepath': filepath,
                                'new_format': new_format
                            },
                            processstep=convert_files_step,
                            information_package=ip,
                            responsible=self.request.user,
                        ))

            ProcessTask.objects.bulk_create(tasks, 1000)

        generate_xml_step = ProcessStep.objects.create(
            name="Generate XML",
            parent_step_pos=20
        )

        for fname, template in filesToCreate.iteritems():
            dirname = os.path.dirname(fname)
            t = ProcessTask.objects.create(
                name="ESSArch_Core.tasks.DownloadSchemas",
                params={
                    "template": template,
                    "dirname": dirname,
                    "structure": structure,
                    "root": ip.object_path,
                },
                processstep_pos=1,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )

            generate_xml_step.add_tasks(t)

        t = ProcessTask.objects.create(
            name="ESSArch_Core.tasks.GenerateXML",
            params={
                "info": info,
                "filesToCreate": filesToCreate,
                "folderToParse": ip_prepare_path,
                "algorithm": ip.get_checksum_algorithm(),
            },
            processstep_pos=3,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        )

        generate_xml_step.add_tasks(t)

        if any(validators.itervalues()):
            validate_step = ProcessStep.objects.create(
                name="Validation", parent_step=main_step,
                parent_step_pos=30,
            )

            if validate_xml_file:
                validate_step.add_tasks(
                    ProcessTask.objects.create(
                        name="ESSArch_Core.tasks.ValidateXMLFile",
                        params={
                            "xml_filename": mets_path,
                            "rootdir": ip.object_path,
                        },
                        processstep_pos=1,
                        log=EventIP,
                        information_package=ip,
                        responsible=self.request.user,
                    )
                )

                if ip.profile_locked("preservation_metadata"):
                    validate_step.add_tasks(
                        ProcessTask.objects.create(
                            name="ESSArch_Core.tasks.ValidateXMLFile",
                            params={
                                "xml_filename": premis_path,
                                "rootdir": ip.object_path,
                            },
                            processstep_pos=2,
                            log=EventIP,
                            information_package=ip,
                            responsible=self.request.user,
                        )
                    )

            if validate_logical_physical_representation:
                validate_step.add_tasks(
                    ProcessTask.objects.create(
                        name="ESSArch_Core.tasks.ValidateLogicalPhysicalRepresentation",
                        params={
                            "dirname": ip.object_path,
                            "xmlfile": mets_path,
                            "rootdir": ip.object_path,
                        },
                        processstep_pos=3,
                        log=EventIP,
                        information_package=ip,
                        responsible=self.request.user,
                    )
                )

            validate_step.add_tasks(
                ProcessTask.objects.create(
                    name="ESSArch_Core.tasks.ValidateFiles",
                    params={
                        "ip": ip.pk,
                        "xmlfile": mets_path,
                        "validate_fileformat": validate_file_format,
                        "validate_integrity": validate_integrity,
                    },
                    processstep_pos=4,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

            validate_step.save()

        info = {
            "_OBJID": ip.object_identifier_value,
            "_OBJLABEL": ip.label
        }

        filesToCreate = OrderedDict()
        filesToCreate[events_path] = get_event_spec()

        create_sip_step = ProcessStep.objects.create(
                name="Create SIP",
                parent_step_pos=40
        )

        create_log_file_step = ProcessStep.objects.create(
            name="Create Log File",
            parent_step_pos=15,
        )
        for fname, template in filesToCreate.iteritems():
            dirname = os.path.dirname(fname)
            create_log_file_step.add_tasks(ProcessTask.objects.create(
                name="ESSArch_Core.tasks.DownloadSchemas",
                params={
                    "template": template,
                    "dirname": dirname,
                    "structure": structure,
                    "root": ip.object_path,
                },
                processstep_pos=-1,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            ))

        create_log_file_step.add_tasks(ProcessTask.objects.create(
            name="ESSArch_Core.tasks.GenerateXML",
            params={
                "info": info,
                "filesToCreate": filesToCreate,
                "algorithm": ip.get_checksum_algorithm(),
            },
            processstep_pos=0,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        create_log_file_step.add_tasks(ProcessTask.objects.create(
            name="ESSArch_Core.tasks.AppendEvents",
            params={
                "filename": events_path,
            },
            processstep_pos=1,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        spec = {
            "-name": "object",
            "-namespace": "premis",
            "-children": [
                {
                    "-name": "objectIdentifier",
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "objectIdentifierType",
                            "-namespace": "premis",
                            "#content": [{"var": "FIDType"}],
                            "-children": []
                        },
                        {
                            "-name": "objectIdentifierValue",
                            "-namespace": "premis",
                            "#content": [{"var": "FID"}],
                            "-children": []
                        }
                    ]
                },
                {
                    "-name": "objectCharacteristics",
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "format",
                            "-namespace": "premis",
                            "-children": [
                                {
                                    "-name": "formatDesignation",
                                    "-namespace": "premis",
                                    "-children": [
                                        {
                                            "-name": "formatName",
                                            "-namespace": "premis",
                                            "#content": [{"var": "FFormatName"}],
                                            "-children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "-name": "storage",
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "contentLocation",
                            "-namespace": "premis",
                            "-children": [
                                {
                                    "-name": "contentLocationType",
                                    "-namespace": "premis",
                                    "#content": [{"var": "FLocationType"}],
                                    "-children": []
                                },
                                {
                                    "-name": "contentLocationValue",
                                    "-namespace": "premis",
                                    "#content": [{"text": "file:///%s.%s" % (ip.object_identifier_value, container_format.lower())}],
                                    "-children": []
                                }
                            ]
                        }
                    ]
                }
            ],
            "-attr": [
                {
                  "-name": "type",
                  '-namespace': 'xsi',
                  "-req": "1",
                  "#content": [{"text": "premis:file"}]
                }
            ],
        }

        info = {
            'FIDType': "UUID",
            'FID': ip.object_identifier_value,
            'FFormatName': container_format.upper(),
            'FLocationType': 'URI',
            'FName': ip.object_path,
        }

        create_log_file_step.add_tasks(ProcessTask.objects.create(
            name="ESSArch_Core.tasks.InsertXML",
            params={
                "filename": events_path,
                "elementToAppendTo": "premis",
                "spec": spec,
                "info": info,
                "index": 0
            },
            processstep_pos=2,
            information_package=ip,
            responsible=self.request.user,
        ))

        if validate_xml_file:
            create_log_file_step.add_tasks(
                ProcessTask.objects.create(
                    name="ESSArch_Core.tasks.ValidateXMLFile",
                    params={
                        "xml_filename": events_path,
                        "rootdir": ip.object_path,
                    },
                    processstep_pos=3,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

        try:
            compress = ip.get_profile('transfer_project').specification_data.get(
                'container_format_compression'
            )
        except AttributeError:
            compress = False

        if container_format.lower() == 'zip':
            zipname = os.path.join(ip_reception_path) + '.zip'
            container_task = ProcessTask.objects.create(
                name="ESSArch_Core.tasks.CreateZIP",
                params={
                    "dirname": ip_prepare_path,
                    "zipname": zipname,
                    "compress": compress
                },
                processstep_pos=4,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )

        else:
            tarname = os.path.join(ip_reception_path) + '.tar'
            container_task = ProcessTask.objects.create(
                name="ESSArch_Core.tasks.CreateTAR",
                params={
                    "dirname": ip_prepare_path,
                    "tarname": tarname,
                    "compress": compress
                },
                processstep_pos=4,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )

        create_sip_step.add_tasks(container_task)

        create_sip_step.add_tasks(
            ProcessTask.objects.create(
                name="ESSArch_Core.tasks.DeleteFiles",
                params={
                    "path": ip.object_path
                },
                processstep_pos=45,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )
        )

        create_sip_step.add_tasks(
            ProcessTask.objects.create(
                name="ESSArch_Core.tasks.UpdateIPPath",
                params={
                    "ip": ip.pk,
                },
                result_params={
                    "path": container_task.pk
                },
                processstep_pos=50,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )
        )

        create_sip_step.add_tasks(
            ProcessTask.objects.create(
                name="ESSArch_Core.tasks.UpdateIPSizeAndCount",
                params={
                    'ip': ip.pk
                },
                processstep_pos=55,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )
        )

        create_sip_step.add_tasks(
            ProcessTask.objects.create(
                name="ESSArch_Core.tasks.UpdateIPStatus",
                params={
                    "ip": ip.pk,
                    "status": "Created",
                },
                processstep_pos=60,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )
        )

        create_sip_step.save()

        main_step.add_child_steps(
            start_create_sip_step, create_log_file_step, generate_xml_step,
            create_sip_step
        )

        if file_conversion:
            main_step.add_child_steps(convert_files_step)

        main_step.information_package = ip
        main_step.save()
        main_step.run()

        return Response({'status': 'creating ip'})

    @detail_route(methods=['post'], url_path='submit', permission_classes=[CanSubmitSIP])
    def submit(self, request, pk=None):
        """
        Submits the specified information package

        Args:
            pk: The primary key (id) of the information package to submit

        Returns:
            None
        """

        ip = self.get_object()

        if ip.state != "Created":
            return Response(
                "The IP (%s) is in the state '%s' but should be 'Created'" % (pk, ip.state),
                status=status.HTTP_400_BAD_REQUEST
            )

        sd_profile = ip.get_profile('submit_description')

        if sd_profile is None:
            return Response(
                "The IP (%s) has no submit description profile" % pk,
                status=status.HTTP_400_BAD_REQUEST
            )


        recipient = ip.get_email_recipient()

        if recipient:
            for arg in ['subject', 'body']:
                if arg not in request.data:
                    raise exceptions.ParseError('%s parameter missing' % arg)

            subject = request.data['subject']
            body = request.data['body']

        validators = request.data.get('validators', {})

        validate_xml_file = validators.get('validate_xml_file', False)
        validate_file_format = validators.get('validate_file_format', False)
        validate_integrity = validators.get('validate_integrity', False)
        validate_logical_physical_representation = validators.get('validate_logical_physical_representation', False)

        step = ProcessStep.objects.create(
            name="Submit SIP",
            information_package=ip,
            eager=False,
        )

        step.add_tasks(ProcessTask.objects.create(
            name="ESSArch_Core.tasks.UpdateIPStatus",
            params={
                "ip": ip.pk,
                "status": "Submitting",
            },
            processstep_pos=0,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        reception = Path.objects.get(entity="path_preingest_reception").value

        container_format = ip.get_container_format()
        container_file = os.path.join(reception, ip.object_identifier_value + ".%s" % container_format.lower())

        sa = ip.submission_agreement

        info = fill_specification_data(ip.get_profile_data('submit_description'), ip=ip, sa=sa)
        info["_IP_CREATEDATE"] = timestamp_to_datetime(creation_date(container_file)).isoformat()

        infoxml = os.path.join(reception, ip.object_identifier_value + ".xml")

        filesToCreate = {
            infoxml: sd_profile.specification
        }

        step.add_tasks(ProcessTask.objects.create(
            name="ESSArch_Core.tasks.GenerateXML",
            params={
                "info": info,
                "filesToCreate": filesToCreate,
                "folderToParse": container_file,
                "algorithm": ip.get_checksum_algorithm(),
            },
            processstep_pos=10,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        if validate_xml_file:
            step.add_tasks(
                ProcessTask.objects.create(
                    name="ESSArch_Core.tasks.ValidateXMLFile",
                    params={
                        "xml_filename": infoxml
                    },
                    processstep_pos=14,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

        if validate_file_format or validate_integrity:
            step.add_tasks(
                ProcessTask.objects.create(
                    name="ESSArch_Core.tasks.ValidateFiles",
                    params={
                        "ip": ip.pk,
                        "rootdir": reception,
                        "xmlfile": infoxml,
                        "validate_fileformat": validate_file_format,
                        "validate_integrity": validate_integrity,
                    },
                    processstep_pos=15,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

        if validate_logical_physical_representation:
            step.add_tasks(
                ProcessTask.objects.create(
                    name="ESSArch_Core.tasks.ValidateLogicalPhysicalRepresentation",
                    params={
                        "files": [os.path.basename(ip.object_path)],
                        "xmlfile": infoxml,
                    },
                    processstep_pos=16,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

        step.add_tasks(ProcessTask.objects.create(
            name="preingest.tasks.SubmitSIP",
            params={
                "ip": ip.pk
            },
            processstep_pos=20,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        if recipient:
            attachments = [infoxml]

            step.add_tasks(ProcessTask.objects.create(
                name="ESSArch_Core.tasks.SendEmail",
                params={
                    'sender': self.request.user.email,
                    'recipients': [recipient],
                    'subject': subject,
                    'body': body,
                    'attachments': attachments
                },
                processstep_pos=25,
                information_package=ip,
                responsible=self.request.user
            ))

        step.add_tasks(ProcessTask.objects.create(
            name="ESSArch_Core.tasks.UpdateIPStatus",
            params={
                "ip": ip.pk,
                "status": "Submitted"
            },
            processstep_pos=30,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        step.save()
        step.run()

        return Response({'status': 'submitting ip'})

    @detail_route(methods=['put'], url_path='check-profile')
    def check_profile(self, request, pk=None):
        ip = self.get_object()
        ptype = request.data.get("type")

        try:
            pip = ProfileIP.objects.get(ip=ip, profile__profile_type=ptype)

            if not pip.LockedBy:
                pip.included = request.data.get('checked', not pip.included)
                pip.save()
        except ProfileIP.DoesNotExist:
            print "pip does not exist"
            pass

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
                ip.pk, new_profile
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
        ip.object_path = os.path.join(prepare_path, ip.object_identifier_value)
        ip.save(update_fields=['object_path'])

        return Response({
            'status': 'unlocking profile with type "%s" in IP "%s"' % (
                ptype, ip.pk
            )
        })

    @detail_route(methods=['get', 'post'], url_path='upload', permission_classes=[CanUpload])
    def upload(self, request, pk=None):
        ip = self.get_object()
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

        path = os.path.join(ip.object_path, request.data['path'])

        with open(path, 'wb') as f:
            for chunk_file in natsorted(glob.glob('%s_*' % re.sub(r'([\[\]])', '[\\1]', path))):
                f.write(open(chunk_file).read())
                os.remove(chunk_file)

        event_type = EventType.objects.get(eventType=10120)
        agent = request.user
        create_event(
            event_type, 0, "Uploaded %s" % path,
            get_versions()['version'], agent, ip=ip
        )

        return Response("Merged chunks")

    @detail_route(methods=['post'], url_path='set-uploaded', permission_classes=[CanSetUploaded])
    def set_uploaded(self, request, pk=None):
        ip = self.get_object()
        ip.state = "Uploaded"
        ip.save()

        t = ProcessTask.objects.create(
            name="ESSArch_Core.tasks.UpdateIPSizeAndCount",
            eager=False,
            params={
                'ip': pk
            },
            information_package=ip
        )

        t.run()
        return Response()
