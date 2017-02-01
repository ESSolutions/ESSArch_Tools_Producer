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
from operator import itemgetter

import errno
import glob
import os
import shutil

from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from django.http import HttpResponse
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ESSArch_Core.configuration.models import (
    EventType,
    Path,
)

from ESSArch_Core.essxml.Generator.xmlGenerator import (
    find_destination
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
)

from ESSArch_Core.profiles.models import (
    Profile,
    ProfileIP,
)

from ESSArch_Core.util import (
    create_event,
    creation_date,
    get_event_spec,
    get_files_and_dirs,
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
    InformationPackageDetailSerializer,
    EventIPSerializer,
)

from preingest.serializers import (
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
        'ArchivalInstitution', 'ArchivistOrganization', 'ArchivalType', 'ArchivalLocation',
        'Responsible__user_permissions', 'Responsible__groups__permissions', 'steps',
    ).select_related('SubmissionAgreement')
    serializer_class = InformationPackageSerializer
    filter_backends = (
        filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter,
    )
    ordering_fields = (
        'Label', 'Responsible', 'CreateDate', 'State', 'eventDateTime',
        'eventType', 'eventOutcomeDetailNote', 'eventOutcome',
        'linkingAgentIdentifierValue', 'id'
    )
    search_fields = ('Label', 'Responsible', 'State', 'SubmissionAgreement__sa_name')
    filter_class = InformationPackageFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return InformationPackageSerializer

        return InformationPackageDetailSerializer

    def get_permissions(self):
        if self.action == 'partial_update':
            if self.request.data.get('SubmissionAgreement'):
                self.permission_classes = [CanChangeSA]
        if self.action == 'destroy':
            self.permission_classes = [CanDeleteIP]

        return super(InformationPackageViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = self.queryset

        other = self.request.query_params.get('other')

        if other is not None:
            queryset = queryset.filter(
                ArchivalInstitution=None,
                ArchivistOrganization=None,
                ArchivalType=None,
                ArchivalLocation=None
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

        label = request.data.get('label', None)
        responsible = self.request.user

        prepare_ip(label, responsible).run()
        return Response({"status": "Prepared IP"})

    def destroy(self, request, pk=None):
        ip = self.get_object()
        self.check_object_permissions(request, ip)
        path = ip.ObjectPath

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

        try:
            shutil.rmtree(ip.ObjectPath)
        except:
            pass

        try:
            os.remove(ip.ObjectPath + ".tar")
        except:
            pass

        try:
            os.remove(ip.ObjectPath + ".zip")
        except:
            pass

        return super(InformationPackageViewSet, self).destroy(request, pk=pk)

    @detail_route()
    def events(self, request, pk=None):
        ip = self.get_object()
        events = filters.OrderingFilter().filter_queryset(request, ip.events.all(), self)
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

    @detail_route()
    def files(self, request, pk=None):
        ip = self.get_object()
        entries = []
        path = os.path.join(ip.ObjectPath, request.query_params.get('path', ''))

        for entry in get_files_and_dirs(path):
            entry_type = "dir" if entry.is_dir() else "file"
            entries.append(
                {
                    "name": os.path.basename(entry.path),
                    "type": entry_type
                }
            )

        sorted_entries = sorted(entries, key=itemgetter('name'))
        return Response(sorted_entries)

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
        sa = ip.SubmissionAgreement
        agent = request.user

        if ip.State != "Uploaded":
            raise ValueError(
                "The IP (%s) is in the state '%s' but should be 'Uploaded'" % (pk, ip.State)
            )

        validators = request.data.get('validators', {})

        validate_xml_file = validators.get('validate_xml_file', False)
        validate_file_format = validators.get('validate_file_format', False)
        validate_integrity = validators.get('validate_integrity', False)
        validate_logical_physical_representation = validators.get('validate_logical_physical_representation', False)

        container_format = ip.get_container_format()

        main_step = ProcessStep.objects.create(
            name="Create SIP",
        )

        t0 = ProcessTask.objects.create(
            name="preingest.tasks.UpdateIPStatus",
            params={
                "ip": ip,
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

        start_create_sip_step.tasks.add(t0)

        event_type = EventType.objects.get(eventType=10200)

        create_event(event_type, 0, "Created SIP", get_versions()['version'], agent, ip=ip)

        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        reception_path = Path.objects.get(
            entity="path_preingest_reception"
        ).value

        ip_prepare_path = os.path.join(prepare_path, str(ip.pk))
        ip_reception_path = os.path.join(reception_path, str(ip.pk))
        events_path = os.path.join(ip_prepare_path, "ipevents.xml")

        structure = ip.get_profile('sip').structure

        info = ip.get_profile('sip').fill_specification_data(sa, ip)

        # ensure premis is created before mets
        filesToCreate = OrderedDict()

        if ip.profile_locked('preservation_metadata'):
            premis_profile = ip.get_profile('preservation_metadata')
            premis_dir, premis_name = find_destination("preservation_description_file", structure)
            premis_path = os.path.join(ip.ObjectPath, premis_dir, premis_name)
            filesToCreate[premis_path] = premis_profile.specification

        mets_dir, mets_name = find_destination("mets_file", structure)
        mets_path = os.path.join(ip.ObjectPath, mets_dir, mets_name)
        filesToCreate[mets_path] = ip.get_profile('sip').specification

        generate_xml_step = ProcessStep.objects.create(
            name="Generate XML",
            parent_step_pos=1
        )

        for fname, template in filesToCreate.iteritems():
            dirname = os.path.dirname(fname)
            t = ProcessTask.objects.create(
                name="ESSArch_Core.tasks.DownloadSchemas",
                params={
                    "template": template,
                    "dirname": dirname,
                    "structure": structure,
                    "root": ip.ObjectPath,
                },
                processstep_pos=1,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )

            generate_xml_step.tasks.add(t)

        t = ProcessTask.objects.create(
            name="preingest.tasks.GenerateXML",
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

        generate_xml_step.tasks.add(t)

        if any(validators.itervalues()):
            validate_step = ProcessStep.objects.create(
                name="Validation", parent_step=main_step,
                parent_step_pos=2,
            )

            if validate_xml_file:
                validate_step.tasks.add(
                    ProcessTask.objects.create(
                        name="preingest.tasks.ValidateXMLFile",
                        params={
                            "xml_filename": mets_path,
                        },
                        processstep_pos=1,
                        log=EventIP,
                        information_package=ip,
                        responsible=self.request.user,
                    )
                )

                if ip.profile_locked("preservation_metadata"):
                    validate_step.tasks.add(
                        ProcessTask.objects.create(
                            name="preingest.tasks.ValidateXMLFile",
                            params={
                                "xml_filename": premis_path,
                            },
                            processstep_pos=2,
                            log=EventIP,
                            information_package=ip,
                            responsible=self.request.user,
                        )
                    )

            if validate_logical_physical_representation:
                validate_step.tasks.add(
                    ProcessTask.objects.create(
                        name="preingest.tasks.ValidateLogicalPhysicalRepresentation",
                        params={
                            "dirname": ip.ObjectPath,
                            "xmlfile": mets_path,
                        },
                        processstep_pos=3,
                        log=EventIP,
                        information_package=ip,
                        responsible=self.request.user,
                    )
                )

            validate_step.tasks.add(
                ProcessTask.objects.create(
                    name="preingest.tasks.ValidateFiles",
                    params={
                        "ip": ip,
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
            "_OBJID": str(ip.pk),
            "_OBJLABEL": ip.Label
        }

        filesToCreate = OrderedDict()
        filesToCreate[events_path] = get_event_spec()

        create_sip_step = ProcessStep.objects.create(
                name="Create SIP",
                parent_step_pos=3
        )

        for fname, template in filesToCreate.iteritems():
            dirname = os.path.dirname(fname)
            create_sip_step.tasks.add(ProcessTask.objects.create(
                name="ESSArch_Core.tasks.DownloadSchemas",
                params={
                    "template": template,
                    "dirname": dirname,
                    "structure": structure,
                    "root": ip.ObjectPath,
                },
                processstep_pos=-1,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            ))

        create_sip_step.tasks.add(ProcessTask.objects.create(
            name="preingest.tasks.GenerateXML",
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

        create_sip_step.tasks.add(ProcessTask.objects.create(
            name="preingest.tasks.AppendEvents",
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
                                    "#content": [{"text": "file:///%s.%s" % (ip.pk, container_format.lower())}],
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
            'FID': ip.ObjectIdentifierValue,
            'FFormatName': container_format.upper(),
            'FLocationType': 'URI',
            'FName': ip.ObjectPath,
        }

        create_sip_step.tasks.add(ProcessTask.objects.create(
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
            create_sip_step.tasks.add(
                ProcessTask.objects.create(
                    name="preingest.tasks.ValidateXMLFile",
                    params={
                        "xml_filename": events_path,
                    },
                    processstep_pos=3,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

        if container_format.lower() == 'zip':
            zipname = os.path.join(ip_reception_path) + '.zip'
            container_task = ProcessTask.objects.create(
                name="preingest.tasks.CreateZIP",
                params={
                    "dirname": ip_prepare_path,
                    "zipname": zipname,
                },
                processstep_pos=4,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )

        else:
            tarname = os.path.join(ip_reception_path) + '.tar'
            container_task = ProcessTask.objects.create(
                name="preingest.tasks.CreateTAR",
                params={
                    "dirname": ip_prepare_path,
                    "tarname": tarname,
                },
                processstep_pos=4,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )

        create_sip_step.tasks.add(container_task)

        create_sip_step.tasks.add(
            ProcessTask.objects.create(
                name="preingest.tasks.DeleteFiles",
                params={
                    "path": ip.ObjectPath
                },
                processstep_pos=45,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )
        )

        create_sip_step.tasks.add(
            ProcessTask.objects.create(
                name="preingest.tasks.UpdateIPPath",
                params={
                    "ip": ip,
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

        create_sip_step.tasks.add(
            ProcessTask.objects.create(
                name="preingest.tasks.UpdateIPStatus",
                params={
                    "ip": ip,
                    "status": "Created",
                },
                processstep_pos=60,
                log=EventIP,
                information_package=ip,
                responsible=self.request.user,
            )
        )

        create_sip_step.save()

        main_step.child_steps.add(
            start_create_sip_step, generate_xml_step, create_sip_step
        )
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

        if ip.State != "Created":
            raise ValueError(
                "The IP (%s) is in the state '%s' but should be 'Created'" % (pk, ip.State)
            )

        validators = request.data.get('validators', {})

        validate_xml_file = validators.get('validate_xml_file', False)
        validate_file_format = validators.get('validate_file_format', False)
        validate_integrity = validators.get('validate_integrity', False)
        validate_logical_physical_representation = validators.get('validate_logical_physical_representation', False)

        step = ProcessStep.objects.create(
            name="Submit SIP",
            information_package=ip
        )

        step.tasks.add(ProcessTask.objects.create(
            name="preingest.tasks.UpdateIPStatus",
            params={
                "ip": ip,
                "status": "Submitting",
            },
            processstep_pos=0,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        reception = Path.objects.get(entity="path_preingest_reception").value

        sd_profile = ip.get_profile('submit_description')

        container_format = ip.get_container_format()
        container_file = os.path.join(reception, str(ip.pk) + ".%s" % container_format.lower())

        sa = ip.SubmissionAgreement

        info = sd_profile.fill_specification_data(sa, ip)
        info["_IP_CREATEDATE"] = timestamp_to_datetime(creation_date(container_file)).isoformat()

        infoxml = os.path.join(reception, str(ip.pk) + ".xml")

        filesToCreate = {
            infoxml: sd_profile.specification
        }

        step.tasks.add(ProcessTask.objects.create(
            name="preingest.tasks.GenerateXML",
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
            step.tasks.add(
                ProcessTask.objects.create(
                    name="preingest.tasks.ValidateXMLFile",
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
            step.tasks.add(
                ProcessTask.objects.create(
                    name="preingest.tasks.ValidateFiles",
                    params={
                        "ip": ip,
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
            step.tasks.add(
                ProcessTask.objects.create(
                    name="preingest.tasks.ValidateLogicalPhysicalRepresentation",
                    params={
                        "files": [os.path.basename(ip.ObjectPath)],
                        "xmlfile": infoxml,
                    },
                    processstep_pos=16,
                    log=EventIP,
                    information_package=ip,
                    responsible=self.request.user,
                )
            )

        step.tasks.add(ProcessTask.objects.create(
            name="preingest.tasks.SubmitSIP",
            params={
                "ip": ip
            },
            processstep_pos=20,
            log=EventIP,
            information_package=ip,
            responsible=self.request.user,
        ))

        if ip.get_email_recipient():
            recipients = [ip.get_email_recipient()]
            subject = request.data.get('subject')
            body = request.data.get('body')

            attachments = [ip.ObjectPath]

            step.tasks.add(ProcessTask.objects.create(
                name="ESSArch_Core.tasks.SendEmail",
                params={
                    'sender': self.request.user.email,
                    'recipients': recipients,
                    'subject': subject,
                    'body': body,
                    'attachments': attachments
                },
                processstep_pos=25,
                information_package=ip,
                responsible=self.request.user
            ))

        step.tasks.add(ProcessTask.objects.create(
            name="preingest.tasks.UpdateIPStatus",
            params={
                "ip": ip,
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

        ip.change_profile(new_profile)

        return Response({
            'status': 'updating IP (%s) with new profile (%s)' % (
                ip.pk, new_profile
            )
        })

    @detail_route(methods=['post'], url_path='unlock-profile', permission_classes=[CanUnlockProfile])
    def unlock_profile(self, request, pk=None):
        ip = self.get_object()
        ptype = request.data.get("type")

        if ptype:
            ip.unlock_profile(ptype)
            return Response({
                'status': 'unlocking profile with type "%s" in IP "%s"' % (
                    ptype, ip.pk
                )
            })

        return Response()

    @detail_route(methods=['get', 'post'], url_path='upload')
    def upload(self, request, pk=None):
        ip = self.get_object()
        ip.State = "Uploading"
        ip.save()
        dst, _ = find_destination('content', ip.get_profile('sip').structure)

        if dst is None:
            dst = ''

        if request.method == 'GET':
            path = os.path.join(dst, request.GET.get('flowRelativePath', ''))
            chunk_nr = request.GET.get('flowChunkNumber')
            chunk_path = "%s_%s" % (path, chunk_nr)

            if os.path.exists(os.path.join(ip.ObjectPath, chunk_path)):
                return HttpResponse(status=200)
            return HttpResponse(status=204)

        if request.method == 'POST':
            path = os.path.join(dst, request.data.get('flowRelativePath', ''))
            chunk_nr = request.data.get('flowChunkNumber')
            chunk_path = "%s_%s" % (path, chunk_nr)
            chunk_path = os.path.join(ip.ObjectPath, chunk_path)

            chunk = request.FILES['file']

            if not os.path.exists(os.path.dirname(chunk_path)):
                mkdir_p(os.path.dirname(chunk_path))

            with open(chunk_path, 'wb+') as dst:
                for c in chunk.chunks():
                    dst.write(c)

            if chunk_nr == request.data.get('flowTotalChunks'):
                path = os.path.join(ip.ObjectPath, path)

                with open(path, 'wb') as f:
                    for chunk_file in glob.glob('%s_*' % path):
                        f.write(open(chunk_file).read())
                        os.remove(chunk_file)

                event_type = EventType.objects.get(eventType=10120)
                agent = request.user
                create_event(
                    event_type, 0, "Uploaded %s" % path,
                    get_versions()['version'], agent, ip=ip
                )

            return Response("Uploaded files")

    @detail_route(methods=['post'], url_path='set-uploaded', permission_classes=[CanSetUploaded])
    def set_uploaded(self, request, pk=None):
        ip = self.get_object()
        ip.State = "Uploaded"
        ip.save()
        return Response()


class EventIPViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = EventIP.objects.all()
    serializer_class = EventIPSerializer
    filter_backends = (
        filters.OrderingFilter, DjangoFilterBackend,
    )
    ordering_fields = (
        'id', 'eventType', 'eventOutcomeDetailNote', 'eventOutcome',
        'linkingAgentIdentifierValue', 'eventDateTime',
    )

    def create(self, request):
        """
        """

        outcomeDetailNote = request.data.get('eventOutcomeDetailNote', None)
        outcome = request.data.get('eventOutcome', 0)
        type_id = request.data.get('eventType', None)
        ip_id = request.data.get('information_package', None)

        eventType = EventType.objects.get(pk=type_id)
        ip = InformationPackage.objects.get(pk=ip_id)
        agent = request.user

        EventIP.objects.create(
            eventOutcome=outcome, eventOutcomeDetailNote=outcomeDetailNote,
            eventType=eventType, linkingObjectIdentifierValue=ip,
            linkingAgentIdentifierValue=agent
        )
        return Response({"status": "Created event"})
