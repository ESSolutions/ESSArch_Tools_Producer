#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
'''
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2013  ES Solutions AB

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
'''

import django
django.setup()

import json
import os
import uuid

from django.conf import settings

# own models etc
from ESSArch_Core.configuration.models import (
    EventType
)

from ESSArch_Core.ip.models import (
    EventIP,
    InformationPackage,
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
)

from ESSArch_Core.WorkflowEngine.models import (
    ProcessStep,
    ProcessTask,
)

from ip.steps import (
    prepare_ip,
)

from ESSArch_Core.profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileSA,
)

# settings
site_profile = "SE" # SE_NEW, SE, NO, EC
#zone = "zone1" # ETP=zone1, ETA=zone2


def installProfiles(): # Install all different profiles
    # First remove all existing data
    EventIP.objects.all().delete()
    ArchivalInstitution.objects.all().delete()
    ArchivistOrganization.objects.all().delete()
    ArchivalType.objects.all().delete()
    ArchivalLocation.objects.all().delete()
    InformationPackage.objects.all().delete()
    SubmissionAgreement.objects.all().delete()
    Profile.objects.all().delete()
    ProcessStep.objects.all().delete()
    ProcessTask.objects.all().delete()

    # install default configuration
    installProfileTransferProject()   		# Profile Transfer Project
    installProfileContentType()         	# Profile Content Type
    installProfileDataSelection()       	# Profile Data Selection
    installProfileClassification()      	# Profile Classification
    installProfileImport()              	# Profile Import
    installProfileSubmitDescription()   	# Profile Submit Description
    installProfileSIP()				# Profile Submission Information Package
    installProfileAIP()  			# Profile Archival Information Package
    installProfileDIP()				# Profile Dissemination Information Package
    installProfileWorkflow()			# Profile Workflow
    installProfilePreservationMetadata()		# Profile Preservation Metadata
    installProfileEvent()		        # Profile Event
    installSubmissionAgreement()     		# Submission Agreement

    return 0


def installIPs():
    installArchivalInstitution()                # Archival Institution
    installArchivistOrganization()              # Archivist Organization
    installArchivalType()                       # Archival Type
    installArchivalLocation()                   # Archival Location
    installInformationPackages()                # Information Package
    # installEventIPs()                           # Events

    return 0

def installSubmissionAgreement():

    # create submission agreement dictionaries
    dct = {
	  'id': '550e8400-e29b-41d4a716-446655440000',
	  'sa_name': 'SA National Archive xx and Government x',
	  'sa_type': 'Standard',
	  'sa_status': 'Agreed',
	  'sa_label': 'Submission Agreement Naxx and Government x',
	  'sa_cm_version': '1.0',
	  'sa_cm_release_date': '2012-04-26T12:45:00+01:00',
	  'sa_cm_change_authority': 'Ozzy Osbourne, NAxx',
	  'sa_cm_change_description': 'Original',
	  'sa_cm_sections_affected': 'None',
	  'sa_producer_organization': 'Government x',
	  'sa_producer_main_name': 'Elton John',
	  'sa_producer_main_address': 'Bourbon Street 123, City x, Country y',
	  'sa_producer_main_phone': '46 (0)8-123450',
	  'sa_producer_main_email': 'Elton.John@company.se',
	  'sa_producer_main_additional': 'Responsible for contract',
	  'sa_producer_individual_name': 'Mike Oldfield',
	  'sa_producer_individual_role': 'Archivist',
	  'sa_producer_individual_phone': '46 (0)8-123451',
	  'sa_producer_individual_email': 'Mike.Oldfield@company.se',
	  'sa_producer_individual_additional': 'Principal archivist',
	  'sa_archivist_organization': 'National Archive xx',
	  'sa_archivist_main_name': 'Ozzy Osbourne',
	  'sa_archivist_main_address': 'Main street 123, City x, Country y',
	  'sa_archivist_main_phone': '46 (0)8-1001001',
	  'sa_archivist_main_email': 'Ozzy.Osbourne@archive.org',
	  'sa_archivist_main_additional': 'Responsible for contract',
	  'sa_archivist_individual_name': 'Lita Ford',
	  'sa_archivist_individual_role': 'Archivist',
	  'sa_archivist_individual_phone': '46 (0)8-1001002',
	  'sa_archivist_individual_email': 'Lita.Ford@archive.org',
	  'sa_archivist_individual_additional': 'Principal archivist',
	  'sa_designated_community_description': 'Designated community description',
	  'sa_designated_community_individual_name': 'Elvis Presley',
	  'sa_designated_community_individual_role': 'Artist',
	  'sa_designated_community_individual_phone': '46 (0)8-2002001',
	  'sa_designated_community_individual_email': 'Elvis.Presley@xxx.org',
	  'sa_designated_community_individual_additional': 'Celebrity',
    }

    # create according to model with many fields
    sa = SubmissionAgreement.objects.create(**dct)

    ProfileSA.objects.bulk_create([
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440001"
            ),
            submission_agreement=sa,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440007"
            ),
            submission_agreement=sa,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440012"
            ),
            submission_agreement=sa,
        ),
    ])

    #logger.info('Installed Submission Agreement')
    print 'Installed submission agreement'

    return 0

def installProfileTransferProject(): # Profile Transfer Project

    # create profile transfer project dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440001',
        'name': 'SE ERMS Delivery',
        'profile_type': 'transfer_project',
        'type': 'Implementation',
        'status': 'Agreed',
        'label': 'Example of SIP for delivery of SE ERMS',
        'schemas': {},
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Transfer Project')
    print 'Installed profile transfer project'

    return 0

def installProfileContentType(): # Profile Content Type

    # create profile content type dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440002',
        'name': 'SE ERMS',
        'profile_type': 'content_type',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Content based on SE ERMS specification',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Content Type')
    print 'Installed profile content type'

    return 0

def installProfileDataSelection(): # Profile Data Selection

    # create profile data selection dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440003',
        'name': 'Classification of business system xx',
        'profile_type': 'data_selection',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Data selection of business system xx',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Data Selection')
    print 'Installed profile data selection'

    return 0

def installProfileClassification(): # Profile Classification

    # create profile classification dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440004',
        'name': 'Classification of archived objects',
        'profile_type': 'classification',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Classification of archived content',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Classification')
    print 'Installed profile classification'

    return 0

def installProfileImport(): # Profile Import

    # create profile import dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440005',
        'name': 'Transformation import profile for system xx',
        'profile_type': 'import',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Transformation from system x to specification y',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Import')
    print 'Installed profile import'

    return 0

def installProfileSubmitDescription(): # Profile Submit Description

    # create profile submit description dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440006',
        'name': 'Submit description of a single SIP',
        'profile_type': 'submit_description',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Desription of a one2one SIP2AIP',
        'template': [
            {
                "templateOptions": {
                    "type": "text",
                    "label": "ID"
                },
                "type": "input",
                "key": "ID"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "OBJID"
                },
                "type": "input",
                "key": "OBJID"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "LABEL"
                },
                "type": "input",
                "key": "LABEL"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "PROFILE"
                },
                "type": "input",
                "key": "PROFILE"
            }
        ],
        'specification': {
            
        },
        'specification_data': {
            "PROFILE": "your default profile",
            "LABEL": "my default label",
            "OBJID": "a default obj id",
            "ID": "the default id"
        },
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Submit Description')
    print 'Installed profile submit description'

    return 0


def installProfileSIP(): # Profile Submission Information Package

    # create profile submission information package dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440007',
        'name': 'EC',
        'profile_type': 'sip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'SIP profile for SE submissions',
        'representation_info': 'Documentation 1',
        'preservation_descriptive_info': 'Documentation 2',
        'supplemental': 'Documentation 3',
        'access_constraints': 'Documentation 4',
        'datamodel_reference': 'Documentation 5',
        'additional': 'Documentation 6',
        'submission_method': 'Electronically',
        'submission_schedule': 'Once',
        'submission_data_inventory': 'According to submit description',
        "structure": [
            {
                "use": "mets_file",
                "type": "file",
                "name": "mets.xml"
            },
            {
                "type": "folder",
                "name": "metadata",
                "children": [
                    {
                        "type": "folder",
                        "name": "administrative",
                        "children": [
                            {
                                "use": "preservation_description_file",
                                "type": "file",
                                "name": "premis.xml"
                            }
                        ]
                    },
                    {
                        "type": "folder",
                        "name": "descriptive",
                        "children": [
                            {
                                "use": "archival_description_file",
                                "type": "file",
                                "name": "_ARCHIVAL_DESCRIPTION_FILE"
                            },
                            {
                                "use": "authoritive_information_file",
                                "type": "file",
                                "name": "_AUTHORITIVE_INFORMATION_FILE"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "folder",
                "name": "representations",
                "children": [
                    {
                        "type": "folder",
                        "name": "rep-001",
                        "children": [
                            {
                                "type": "folder",
                                "name": "data",
                                "children": []
                            }
                        ]
                    }
                ]
            },
            {
                "type": "folder",
                "name": "schemas",
                "children": [
                    {
                        "use": "xsd_files",
                        "type": "file",
                        "name": "xsd_files"
                    }
                ]
            },
            {
                "type": "folder",
                "name": "documents",
                "children": []
            }
        ],
        'template': [
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.ID"
                },
                "type": "input",
                "key": "mets.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.OBJID"
                },
                "type": "input",
                "key": "mets.OBJID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.LABEL"
                },
                "type": "input",
                "key": "mets.LABEL"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.TYPE"
                },
                "type": "input",
                "key": "mets.TYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.PROFILE"
                },
                "type": "input",
                "key": "mets.PROFILE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.ID"
                },
                "type": "input",
                "key": "mets.metsHdr.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.ADMID"
                },
                "type": "input",
                "key": "mets.metsHdr.ADMID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.CREATEDATE"
                },
                "type": "input",
                "key": "mets.metsHdr.CREATEDATE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.LASTMODDATE"
                },
                "type": "input",
                "key": "mets.metsHdr.LASTMODDATE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.RECORDSTATUS"
                },
                "type": "input",
                "key": "mets.metsHdr.RECORDSTATUS"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Agent Organization"
                },
                "type": "input",
                "key": "agentname1"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.agent.ROLE"
                },
                "type": "input",
                "key": "mets.metsHdr.agent.ROLE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.agent.OTHERROLE"
                },
                "type": "input",
                "key": "mets.metsHdr.agent.OTHERROLE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.agent.TYPE"
                },
                "type": "input",
                "key": "mets.metsHdr.agent.TYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.agent.OTHERTYPE"
                },
                "type": "input",
                "key": "mets.metsHdr.agent.OTHERTYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.agent.name.content"
                },
                "type": "input",
                "key": "mets.metsHdr.agent.name.content"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.agent.note.content"
                },
                "type": "input",
                "key": "mets.metsHdr.agent.note.content"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.altRecordID.content"
                },
                "type": "input",
                "key": "mets.metsHdr.altRecordID.content"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.altRecordID.ID"
                },
                "type": "input",
                "key": "mets.metsHdr.altRecordID.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.altRecordID.TYPE"
                },
                "type": "input",
                "key": "mets.metsHdr.altRecordID.TYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.metsDocumentID.content"
                },
                "type": "input",
                "key": "mets.metsHdr.metsDocumentID.content"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.metsDocumentID.ID"
                },
                "type": "input",
                "key": "mets.metsHdr.metsDocumentID.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.metsHdr.metsDocumentID.TYPE"
                },
                "type": "input",
                "key": "mets.metsHdr.metsDocumentID.TYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.amdSec.ID"
                },
                "type": "input",
                "key": "mets.amdSec.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.amdSec.digiprovMD.ID"
                },
                "type": "input",
                "key": "mets.amdSec.digiprovMD.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.amdSec.digiprovMD.GROUPID"
                },
                "type": "input",
                "key": "mets.amdSec.digiprovMD.GROUPID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.amdSec.digiprovMD.ADMID"
                },
                "type": "input",
                "key": "mets.amdSec.digiprovMD.ADMID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.amdSec.digiprovMD.CREATED"
                },
                "type": "input",
                "key": "mets.amdSec.digiprovMD.CREATED"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.amdSec.digiprovMD.STATUS"
                },
                "type": "input",
                "key": "mets.amdSec.digiprovMD.STATUS"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.fileSec.ID"
                },
                "type": "input",
                "key": "mets.fileSec.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.fileSec.fileGrp.ID"
                },
                "type": "input",
                "key": "mets.fileSec.fileGrp.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.fileSec.fileGrp.VERSDATE"
                },
                "type": "input",
                "key": "mets.fileSec.fileGrp.VERSDATE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.fileSec.fileGrp.ADMID"
                },
                "type": "input",
                "key": "mets.fileSec.fileGrp.ADMID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.fileSec.fileGrp.USE"
                },
                "type": "input",
                "key": "mets.fileSec.fileGrp.USE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.ID"
                },
                "type": "input",
                "key": "mets.structMap.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.TYPE"
                },
                "type": "input",
                "key": "mets.structMap.TYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.LABEL"
                },
                "type": "input",
                "key": "mets.structMap.LABEL"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.ID"
                },
                "type": "input",
                "key": "mets.structMap.div.ID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.ORDER"
                },
                "type": "input",
                "key": "mets.structMap.div.ORDER"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.ORDERLABEL"
                },
                "type": "input",
                "key": "mets.structMap.div.ORDERLABEL"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.LABEL"
                },
                "type": "input",
                "key": "mets.structMap.div.LABEL"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.DMDID"
                },
                "type": "input",
                "key": "mets.structMap.div.DMDID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.ADMID"
                },
                "type": "input",
                "key": "mets.structMap.div.ADMID"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.TYPE"
                },
                "type": "input",
                "key": "mets.structMap.div.TYPE"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "mets.structMap.div.CONTENTIDS"
                },
                "type": "input",
                "key": "mets.structMap.div.CONTENTIDS"
            },
        ],
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/JSONTemplate.json')).read()),
        'specification_data': {
            "xmlns:mets": "http://www.loc.gov/METS/",
            "xmlns:ext": "ExtensionMETS",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd "
            "ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd",
            "xsi:schemaLocationPremis": "http://www.loc.gov/premis/v3 https://www.loc.gov/standards/premis/premis.xsd",
            "mets.PROFILE": "http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xmll",
            "mets.LABEL": "Test of SIP 1",
            "mets.TYPE": "Personnel",
            "mets.OBJID": "UUID:9bc10faa-3fff-4a8f-bf9a-638841061065",
            "ext:CONTENTTYPESPECIFICATION": "FGS Personal, version 1",
            "mets.metsHdr.CREATEDATE": "2016-06-08T10:44:00+02:00",
            "mets.ID": "ID" + str(uuid.uuid4()),
            "mets.metsHdr.ID": "ID" + str(uuid.uuid4()),
            "mets.metsHdr.LASTMODDATE": "2016-06-08T10:44:00+02:00",
            "mets.metsHdr.RECORDSTATUS": "NEW",
            "ext:OAISTYPE": "SIP",
            "agentName": "name",
            "agentNote": "note",
            "REFERENCECODE": "SE/RA/123456/24/F",
            "mets.metsHdr.altRecordID.content": "RA 13-2011/5329, 2012-04-12",
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
            "mets.amdSec.ID": "ID" + str(uuid.uuid4()),
            "mets.amdSec.digiprovMD.ID": "ID" + str(uuid.uuid4()),
            "agentname1": "Government X",
            "agentnote1": "ORG:2010340930",
            "agentname2": "Government X:DEP Y",
            "agentnote2": "ORG:2010340920",
            "agentname3": "HR Employed",
            "agentnote3": "5.0.34",
        }
    }

    dct2 = {
        'id': '550e8400-e29b-41d4a716-446655440017',
        'name': 'SE',
        'profile_type': 'sip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'SIP profile for SE submissions',
        'representation_info': 'Documentation 1',
        'preservation_descriptive_info': 'Documentation 2',
        'supplemental': 'Documentation 3',
        'access_constraints': 'Documentation 4',
        'datamodel_reference': 'Documentation 5',
        'additional': 'Documentation 6',
        'submission_method': 'Electronically',
        'submission_schedule': 'Once',
        'submission_data_inventory': 'According to submit description',
        'structure': [
            {
                'type': 'file',
                'name': 'mets.xml',
                'use': 'mets_file',
            },
            {
                'type': 'folder',
                'name': 'content',
                'children': [
                    {
                        'type': 'file',
                        'name': 'mets_grp',
                        'use': 'mets_grp',
                    },
                    {
                        'type': 'folder',
                        'name': 'data',
                        'children': [],
                    },
                    {
                        'type': 'folder',
                        'name': 'metadata',
                        'children': [],
                    },
                ]
            },
            {
                'type': 'folder',
                'name': 'metadata',
                'children': [
                    {
                        'type': 'file',
                        'use': 'xsd_files',
                        'name': 'xsd_files'
                    },
                    {
                        'type': 'file',
                        'name': 'premis.xml',
                        'use': 'preservation_description_file',
                    },
                    {
                        'type': 'file',
                        'name': '_ARCHIVAL_DESCRIPTION_FILE',
                        'use': 'archival_description_file',
                    },
                    {
                        'type': 'file',
                        'name': '_AUTHORITIVE_INFORMATION_FILE',
                        'use': 'authoritive_information_file',
                    },
                ]
            },
        ],
        'template': [
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xmlns:mets",
                    'disabled': True,
                },
                "type": "input",
                "key": "xmlns:mets",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xmlns:ext",
                    'disabled': True,
                },
                "type": "input",
                "key": "xmlns:ext",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xmlns:xlink",
                    'disabled': True,
                },
                "type": "input",
                "key": "xmlns:xlink",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xmlns:xsi",
                    'disabled': True,
                },
                "type": "input",
                "key": "xmlns:xsi",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xsi:schemaLocation",
                    'disabled': True,
                },
                "type": "input",
                "key": "xsi:schemaLocation"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xsi:schemaLocationPremis",
                    'disabled': True,
                },
                "type": "input",
                "key": "xsi:schemaLocationPremis",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "PROFILE",
                    'disabled': True,
                },
                "type": "input",
                "key": "PROFILE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "LABEL",
                    'disabled': True,
                },
                "type": "input",
                "key": "LABEL",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "TYPE"
                },
                "type": "input",
                "key": "TYPE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "OBJID",
                    'disabled': True,
                },
                "type": "input",
                "key": "OBJID",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "ext:CONTENTTYPESPECIFICATION"
                },
                "type": "input",
                "key": "ext:CONTENTTYPESPECIFICATION",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "CREATEDATE",
                    'disabled': True,
                },
                "type": "input",
                "key": "CREATEDATE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "RECORDSTATUS"
                },
                "type": "input",
                "key": "RECORDSTATUS",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "ext:OAISTYPE"
                },
                "type": "input",
                "key": "ext:OAISTYPE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "agentName"
                },
                "type": "input",
                "key": "agentName",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "agentNote"
                },
                "type": "input",
                "key": "agentNote",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "REFERENCECODE"
                },
                "type": "input",
                "key": "REFERENCECODE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "SUBMISSIONAGREEMENT"
                },
                "type": "input",
                "key": "SUBMISSIONAGREEMENT",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "MetsIdentifier"
                },
                "type": "input",
                "key": "MetsIdentifier",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "filename"
                },
                "type": "input",
                "key": "filename",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "SMLabel"
                },
                "type": "input",
                "key": "SMLabel",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "amdLink",
                    'disabled': True,
                },
                "type": "input",
                "key": "amdLink",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "digiprovLink",
                    'disabled': True,
                },
                "type": "input",
                "key": "digiprovLink",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "LOCTYPE"
                },
                "type": "input",
                "key": "LOCTYPE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "MDTYPE",
                    'disabled': True,
                },
                "type": "input",
                "key": "MDTYPE",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xlink:href",
                    'disabled': True,
                },
                "type": "input",
                "key": "xlink:href",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "xlink:type",
                    'disabled': True,
                },
                "type": "input",
                "key": "xlink:type",
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "ID",
                    'disabled': True,
                },
                "type": "input",
                "key": "ID",
            },
            {
                "key": "agents",
                "fieldGroup": [
                    {
                        "key": "agent_1",
                        #"className": "display-flex",
                        "fieldGroup": [
                            {
                                "type": "input",
                                "key": "ROLE",
                                "templateOptions": {
                                    "label": "ROLE"
                                }
                            },
                            {
                                "type": "input",
                                "key": "TYPE",
                                "templateOptions": {
                                    "label": "TYPE"
                                }
                            },
                            {
                                "type": "input",
                                "key": "OTHERTYPE",
                                "templateOptions": {
                                    "label": "OTHERTYPE"
                                }
                            },
                            {
                                "type": "input",
                                "key": "name",
                                "templateOptions": {
                                    "label": "name"
                                }
                            },
                            {
                                "type": "input",
                                "key": "note",
                                "templateOptions": {
                                    "label": "note"
                                }
                            }
                        ]
                    },
                    {
                        "key": "agent_2",
                        #"className": "display-flex",
                        "fieldGroup": [
                            {
                                "type": "input",
                                "key": "ROLE",
                                "templateOptions": {
                                    "label": "ROLE"
                                }
                            },
                            {
                                "type": "input",
                                "key": "TYPE",
                                "templateOptions": {
                                    "label": "TYPE"
                                }
                            },
                            {
                                "type": "input",
                                "key": "OTHERTYPE",
                                "templateOptions": {
                                    "label": "OTHERTYPE"
                                }
                            },
                            {
                                "type": "input",
                                "key": "name",
                                "templateOptions": {
                                    "label": "name"
                                }
                            },
                            {
                                "type": "input",
                                "key": "note",
                                "templateOptions": {
                                    "label": "note"
                                }
                            }
                        ]
                    }
                ]
            },
        ],
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/JSONTemplate.json')).read()),
        'specification_data': {
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
            "agents": {
                "agent_1": {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "ORGANIZATION",
                    "OTHERTYPE": "",
                    "name": "Arkivbildar namn",
                    "note": "VAT:SE201345098701"
                },
                "agent_2": {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "OTHER",
                    "OTHERTYPE": "SOFTWARE",
                    "name": "By hand Systems",
                    "note": "1.0.0"
                }
            }
        }
    }

    # create according to model with many fields
    Profile.objects.create(**dct)
    Profile.objects.create(**dct2)

    #logger.info('Installed Profile SIP')
    print 'Installed profile SIP'

    return 0


def installProfileAIP(): # Profile Archival Information Package

    # create profile archival information package dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440008',
        'name': 'AIP based on SE FGS Package',
        'profile_type': 'aip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'AIP profile for SE Packages',
        'representation_info': 'Documentation 1',
        'preservation_descriptive_info': 'Documentation 2',
        'supplemental': 'Documentation 3',
        'access_constraints': 'Documentation 4',
        'datamodel_reference': 'Documentation 5',
        'additional': 'Documentation 6',
        'submission_method': 'Electronically',
        'submission_schedule': 'Once',
        'submission_data_inventory': 'According to submit description',
        'structure': 'AIP SE structure xx',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile AIP')
    print 'Installed profile AIP'

    return 0


def installProfileDIP(): # Profile Dissemination Information Package

    # create profile dissemination information package dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440009',
        'name': 'DIP based on SE FGS Package',
        'profile_type': 'dip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'DIP profile for SE Packages',
        'representation_info': 'Documentation 1',
        'preservation_descriptive_info': 'Documentation 2',
        'supplemental': 'Documentation 3',
        'access_constraints': 'Documentation 4',
        'datamodel_reference': 'Documentation 5',
        'additional': 'Documentation 6',
        'submission_method': 'Electronically',
        'submission_schedule': 'Once',
        'submission_data_inventory': 'According to submit description',
        'structure': 'DIP SE structure xx',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile DIP')
    print 'Installed profile DIP'

    return 0


def installProfileWorkflow(): # Profile Workflow

    # create profile workflow dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440010',
        'name': 'Workflow xx for Pre-Ingest',
        'profile_type': 'workflow',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Workflow Create SIP for Pre-Ingest',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Workflow')
    print 'Installed profile workflow'

    return 0


def installProfilePreservationMetadata(): # Profile Preservation Metadata

    # create profile preservation metadata dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440011',
        'name': 'Preservation profile xx',
        'profile_type': 'preservation_metadata',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Preservation profile for AIP xxyy',
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/JSONPremisTemplate.json')).read()),
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile PreservationMetadata')
    print 'Installed profile preservation metadata'

    return 0


def installProfileEvent(): # Profile Event

    # create profile event dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440012',
        'name': 'Event profile xx',
        'profile_type': 'event',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Event profile for SIP xxyyzz',
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/JSONPremisEventTemplate.json')).read()),
        'specification_data': {
            "xmlns:mets": "http://www.loc.gov/METS/",
            "xmlns:premis": "http://www.loc.gov/premis/v3",
            "xmlns:ext": "ExtensionMETS",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd "
            "ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd",
            "xsi:schemaLocationPremis": "http://www.loc.gov/premis/v3 https://www.loc.gov/standards/premis/premis.xsd",
            "PROFILE": "http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xmll",
            "LABEL": "Test of SIP 1",
            "TYPE": "Personnel",
            "premis.version": "3.0",
            "OBJID": "UUID:9bc10faa-3fff-4a8f-bf9a-638841061065",
            "ext:CONTENTTYPESPECIFICATION": "FGS Personal, version 1",
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
            "archival_institution"
            "agents": {
                "agent_1": {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "ORGANIZATION",
                    "OTHERTYPE": "",
                    "name": "Arkivbildar namn",
                    "note": "VAT:SE201345098701"
                },
                "agent_2": {
                    "ROLE": "ARCHIVIST",
                    "TYPE": "OTHER",
                    "OTHERTYPE": "SOFTWARE",
                    "name": "By hand Systems",
                    "note": "1.0.0"
                }
            }
        }
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Event')
    print 'Installed profile event'

    return 0


def installArchivalInstitution():
    lst = [
        {
            'id': 'aa8e20d9-8794-4f26-9859-c3341a31f111',
            'name': 'RA1'
        },
        {
            'id': 'aa8e20d9-8794-4f26-9859-c3341a31f112',
            'name': 'RA2'
        },
        {
            'id': 'aa8e20d9-8794-4f26-9859-c3341a31f113',
            'name': 'RA3'
        },
    ]

    for dct in lst:
        ArchivalInstitution.objects.create(**dct)

    print "Installed archival institutions"


def installArchivistOrganization():
    lst = [
        {
            'id': '2fe86f14-9b09-46e3-b272-a6e971b9d4e1',
            'name': 'Producer 1'
        },
        {
            'id': '2fe86f14-9b09-46e3-b272-a6e971b9d4e2',
            'name': 'Producer 2'
        },
        {
            'id': '2fe86f14-9b09-46e3-b272-a6e971b9d4e3',
            'name': 'Producer 3'
        },
    ]

    for dct in lst:
        ArchivistOrganization.objects.create(**dct)

    print "Installed archivist organization"


def installArchivalType():
    lst = [
        {
            'id': 'fc3f23aa-203c-4aee-bb20-92373a5eba81',
            'name': 'Dokument'
        },
        {
            'id': 'fc3f23aa-203c-4aee-bb20-92373a5eba82',
            'name': 'Dossier'
        },
        {
            'id': 'fc3f23aa-203c-4aee-bb20-92373a5eba83',
            'name': 'Fotografi'
        },
    ]

    for dct in lst:
        ArchivalType.objects.create(**dct)

    print "Installed archival type"


def installArchivalLocation():
    lst = [
        {
            'id': '83f1f65d-7be0-4577-ade9-543c815417b1',
            'name': 'Stockholm'
        },
        {
            'id': '83f1f65d-7be0-4577-ade9-543c815417b2',
            'name': 'Göteborg'
        },
        {
            'id': '83f1f65d-7be0-4577-ade9-543c815417b3',
            'name': 'Malmö'
        },
    ]

    for dct in lst:
        ArchivalLocation.objects.create(**dct)

    print "Installed archival locations"


def installInformationPackages():
    lst = [
        {
            'label': 'Arkiv 1',
            'responsible': 'Freddie Mercury',
        },
        {
            'label': 'Arkiv 2',
            'responsible': 'Roger Taylor',
        },
        {
            'label': 'Arkiv 3',
            'responsible': 'Brian May',
        },
    ]

    # create according to model with many fields
    for dct in lst:
        prepare_ip(**dct).run()

    print 'Installed information packages'

    return 0

if __name__ == '__main__':
    installProfiles()
    installIPs()
