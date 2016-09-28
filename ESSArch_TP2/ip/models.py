"""
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2016  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
"""

# Create your models here.
from collections import OrderedDict

from django.conf import settings
from django.db import models

from configuration.models import (
    Path,
)

from preingest.models import (
    ProcessStep, ProcessTask,
)

from profiles.models import (
    ProfileLock, SubmissionAgreement as SA
)

import json, os, uuid


class ArchivalInstitution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivalInstitution'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class ArchivistOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivistOrganization'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class ArchivalType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivalType'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class ArchivalLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivalLocation'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class InformationPackage(models.Model):
    """
    Informaion Package
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    Label = models.CharField(max_length=255)
    Content = models.CharField(max_length=255)
    Responsible = models.CharField(max_length=255)
    CreateDate = models.DateTimeField(auto_now_add=True)
    State = models.CharField(max_length=255)
    ObjectSize = models.CharField(max_length=255)
    ObjectNumItems = models.CharField(max_length=255)
    ObjectPath = models.CharField(max_length=255)
    Startdate = models.DateTimeField(null=True)
    Enddate = models.DateTimeField(null=True)
    OAIStype = models.CharField(max_length=255)
    SubmissionAgreement = models.ForeignKey(
        SA,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True,
    )
    ArchivalInstitution = models.ForeignKey(
        ArchivalInstitution,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )
    ArchivistOrganization = models.ForeignKey(
        ArchivistOrganization,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )
    ArchivalType = models.ForeignKey(
        ArchivalType,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )
    ArchivalLocation = models.ForeignKey(
        ArchivalLocation,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )

    def create(self, include_premis=False):
        info = {
            "xmlns:mets": "http://www.loc.gov/METS/",
            "xmlns:ext": "ExtensionMETS",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd "
            "ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd",
            "xsi:schemaLocationPremis": "http://www.loc.gov/premis/v3 https://www.loc.gov/standards/premis/premis.xsd",
            "PROFILE": "http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xmll",
            "LABEL": "Test of SIP 1",
            "TYPE": "Personnel",
            "OBJID": "UUID:9bc10faa-3fff-4a8f-bf9a-638841061065",
            "ext:CONTENTTYPESPECIFICATION": "FGS Personal, version 1",
            "CREATEDATE": "2016-06-08T10:44:00+02:00",
            "RECORDSTATUS": "NEW",
            "ext:OAISTYPE": "SIP",
            "agentName": "name",
            "agentNote": "note",
            "REFERENCECODE": "SE/RA/123456/24/F",
            "SUBMISSIONAGREEMENT": "RA 13-2011/5329, 2012-04-12",
            "MetsIdentifier": "sip.xml",
            "filename": "sip.txt",
            "SMLabel": "Profilestructmap",
            "amdLink": "IDce745fec-cfdd-4d14-bece-d49e867a2487",
            "digiprovLink": "IDa32a20cb-5ff8-4d36-8202-f96519154de2",
            "LOCTYPE": "URL",
            "MDTYPE": "PREMIS",
            "xlink:href": "file:///metadata/premis.xml",
            "xlink:type": "simple",
            "ID": "ID31e51159-9280-44d1-b26c-014077f8eeb5",
            "agents": [
                {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "ORGANIZATION",
                    "name": "Arkivbildar namn",
                    "note": "VAT:SE201345098701"
                }, {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "OTHER",
                    "OTHERTYPE": "SOFTWARE",
                    "name": "By hand Systems",
                    "note": "1.0.0"
                }, {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "OTHER",
                    "OTHERTYPE": "SOFTWARE",
                    "name": "Other By hand Systems",
                    "note": "1.2.0"
                }, {
                    "ROLE": "CREATOR",
                    "TYPE": "ORGANIZATION",
                    "name": "Arkivbildar namn",
                    "note": "HSA:SE2098109810-AF87"
                }, {
                    "ROLE": "OTHER",
                    "OTHERROLE": "PRODUCER",
                    "TYPE": "ORGANIZATION",
                    "name": "Sydarkivera",
                    "note": "HSA:SE2098109810-AF87"
                }, {
                    "ROLE": "OTHER",
                    "OTHERROLE": "SUBMITTER",
                    "TYPE": "ORGANIZATION",
                    "name": "Arkivbildare",
                    "note": "HSA:SE2098109810-AF87"
                }, {
                    "ROLE": "IPOWNER",
                    "TYPE": "ORGANIZATION",
                    "name": "Informations agare",
                    "note": "HSA:SE2098109810-AF87"
                }, {
                    "ROLE": "EDITOR",
                    "TYPE": "ORGANIZATION",
                    "name": "Axenu",
                    "note": "VAT:SE9512114233"
                }, {
                    "ROLE": "CREATOR",
                    "TYPE": "INDIVIDUAL",
                    "name": "Simon Nilsson",
                    "note": "0706758942, simonseregon@gmail.com"
                }
            ],
        }

        # ensure premis is created before mets
        filesToCreate = OrderedDict()

        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        ip_prepare_path = os.path.join(prepare_path, str(self.pk))

        if include_premis:
            premis_path = os.path.join(ip_prepare_path, "premis.xml")
            fname = os.path.join(settings.BASE_DIR, 'templates/JSONPremisTemplate.json')
            with open(fname) as data_file:
                premis_template = json.load(data_file)
            filesToCreate[premis_path] = premis_template

        mets_path = os.path.join(ip_prepare_path, "mets.xml")
        fname = os.path.join(settings.BASE_DIR, 'templates/JSONTemplate.json')
        with open(fname) as data_file:
            mets_template = json.load(data_file)
        filesToCreate[mets_path] = mets_template

        t1 = ProcessTask.objects.create(
            name="preingest.tasks.GenerateXML",
            params={
                "info": info,
                "filesToCreate": filesToCreate,
                "folderToParse": os.path.join(ip_prepare_path, "data")
            },
            processstep_pos=0,
            information_package=self
        )

        generate_xml_step = ProcessStep.objects.create(
            name="Generate XML",
        )
        generate_xml_step.tasks = [t1]
        generate_xml_step.save()

        filename = "foo.csv"
        fileformat = "Comma Seperated Spreadsheet"
        xmlfile = "premis.xml"
        schemafile = "premis.xsd"
        logical = "logical"
        physical = "physical"
        checksum = uuid.uuid4()
        #dirname = os.path.join(ip_prepare_path, "data")
        tarname = os.path.join(ip_prepare_path)
        zipname = os.path.join(ip_prepare_path)

        t2 = ProcessTask.objects.create(
            name="preingest.tasks.ValidateFileFormat",
            params={
                "filename": filename,
                "fileformat": fileformat,
            },
            processstep_pos=0,
            information_package=self
        )

        t3 = ProcessTask.objects.create(
            name="preingest.tasks.ValidateXMLFile",
            params={
                "xml_filename": xmlfile,
                "schema_filename": schemafile,
            },
            processstep_pos=0,
            information_package=self
        )

        t4 = ProcessTask.objects.create(
            name="preingest.tasks.ValidateLogicalPhysicalRepresentation",
            params={
                "logical": logical,
                "physical": physical,
            },
            processstep_pos=0,
            information_package=self
        )

        t5 = ProcessTask.objects.create(
            name="preingest.tasks.ValidateIntegrity",
            params={
                "filename": filename,
                "checksum": checksum,
            },
            processstep_pos=0,
            information_package=self
        )

        validate_step = ProcessStep.objects.create(
            name="Validation",
        )
        validate_step.tasks = [t2, t3, t4, t5]
        validate_step.save()

        t6 = ProcessTask.objects.create(
            name="preingest.tasks.CreateTAR",
            params={
                "dirname": ip_prepare_path,
                "tarname": tarname,
            },
            processstep_pos=0,
            information_package=self
        )

        t7 = ProcessTask.objects.create(
            name="preingest.tasks.CreateZIP",
            params={
                "dirname": ip_prepare_path,
                "zipname": zipname,
            },
            processstep_pos=0,
            information_package=self
        )

        create_sip_step = ProcessStep.objects.create(
                name="Create SIP"
        )
        create_sip_step.tasks = [t6, t7]
        create_sip_step.save()

        main_step = ProcessStep.objects.create(
            name="Create IP",
        )
        main_step.child_steps = [
            generate_xml_step, validate_step, create_sip_step
        ]
        main_step.information_package = self
        main_step.save()
        main_step.run()

    def status(self):
        steps = self.steps.all()

        if steps:
            try:
                progress = sum([s.progress() for s in steps])
                return progress / len(steps)
            except:
                return 0

        return 0

    def locks(self):
        return ProfileLock.objects.filter(
            information_package=self,
            submission_agreement=self.SubmissionAgreement
        )

    class Meta:
        ordering = ["id"]
        verbose_name = 'Information Package'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s' % self.id

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return {
            field.name: field.value_to_string(self)
            for field in InformationPackage._meta.fields
        }


class EventIP(models.Model):
    """
    Events related to IP
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eventType = models.ForeignKey(
        'configuration.EventType',
        on_delete=models.CASCADE
    )
    eventDateTime = models.DateTimeField(auto_now_add=True)
    eventDetail = models.CharField(max_length=255)
    eventApplication = models.CharField(max_length=255)
    eventVersion = models.CharField(max_length=255)
    eventOutcome = models.CharField(max_length=255)
    eventOutcomeDetailNote = models.CharField(max_length=1024)
    linkingAgentIdentifierValue = models.CharField(max_length=255)
    linkingObjectIdentifierValue = models.ForeignKey(
        'InformationPackage',
        on_delete=models.CASCADE,
        related_name='events'
    )

    class Meta:
        ordering = ["eventType"]
        verbose_name = 'Events related to IP'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s (%s)' % (self.eventDetail, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return {
            field.name: field.value_to_string(self)
            for field in EventIP._meta.fields
        }
