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
from django.contrib.auth.models import User

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
    installProfileAuthorityInformation()      	# Profile Authority Information
    installProfileArchivalDescription()      	# Profile Archival Description
    installProfileImport()              	# Profile Import
    installProfileSubmitDescription()   	# Profile Submit Description
    installProfileSIP()				# Profile Submission Information Package
    installProfileAIP()  			# Profile Archival Information Package
    installProfileDIP()				# Profile Dissemination Information Package
    installProfileWorkflow()			# Profile Workflow
    installProfilePreservationMetadata()		# Profile Preservation Metadata
    installSubmissionAgreement()     		# Submission Agreement

    return 0


def installIPs():
    """
    installArchivalInstitution()                # Archival Institution
    installArchivistOrganization()              # Archivist Organization
    installArchivalType()                       # Archival Type
    installArchivalLocation()                   # Archival Location
    """
    # installInformationPackages()                # Information Package
    # installEventIPs()                           # Events

    return 0

def installSubmissionAgreement():

    # create submission agreement dictionaries
    dct = {
	  'sa_name': 'SA National Archive and Government 1',
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
    sa1 = SubmissionAgreement.objects.create(**dct)
    dct['sa_name'] = "SA National Archive and Government 2"
    sa2 = SubmissionAgreement.objects.create(**dct)
    dct['sa_name'] = "SA National Archive and Government 3"
    sa3 = SubmissionAgreement.objects.create(**dct)

    ProfileSA.objects.bulk_create([
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440001"
            ),
            submission_agreement=sa1,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440006"
            ),
            submission_agreement=sa1,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440007"
            ),
            submission_agreement=sa1,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440001"
            ),
            submission_agreement=sa2,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440006"
            ),
            submission_agreement=sa2,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440007"
            ),
            submission_agreement=sa2,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440001"
            ),
            submission_agreement=sa3,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440006"
            ),
            submission_agreement=sa3,
        ),
        ProfileSA(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440007"
            ),
            submission_agreement=sa3,
        ),
    ])

    #logger.info('Installed Submission Agreement')
    print 'Installed submission agreement'

    return 0

def installProfileTransferProject(): # Profile Transfer Project

    # create profile transfer project dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440001',
        'name': 'Transfer Project Profile 1',
        'profile_type': 'transfer_project',
        'type': 'Implementation',
        'status': 'Agreed',
        'label': 'Example of SIP for delivery of SE ERMS',
        'schemas': {},
        'template': [
            {
                "hideExpression": "False",
                "templateOptions": {
                    "type": "text",
                    "label": "Archival institution",
		            "desc": "xxx",
               },
               "type": "input",
               "key": "archival_institution" # Responds to specification data
            }, {
                "hideExpression": "False",
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist organization",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archivist_organization" # Responds to specification data
            }, {
                "hideExpression": "False",
                "templateOptions": {
                    "type": "text",
                    "label": "Archival type",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_type" # Responds to specification data
            }, {
                "hideExpression": "False",
                "templateOptions": {
                    "type": "text",
                    "label": "Archival location",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_location" # Responds to specification data
            }, {
                "hideExpression": "False",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Archive Policy",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archive_policy" # Responds to specification data
            }, {
                'key': 'container_format',
                'type': 'select',
                'templateOptions': {
                  'label': 'Container format',
                  'options': [
                    {'name': 'TAR', 'value': 'tar'},
                    {'name': 'ZIP', 'value': 'zip'},
                  ]
                }
            }, {
                "hideExpression": "False",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Container format compression",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "container_format_compression" # Responds to specification data
            }, {
                'key': 'checksum_algorithm',
                'type': 'select',
                'templateOptions': {
                  'label': 'Checksum algorithm',
                  'options': [
                    {'name': 'MD5', 'value': 'MD5'},
                    {'name': 'SHA-256', 'value': 'SHA-256'},
                  ]
                }
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submission reception validation",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submission_reception_validation" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submission reception exception handling",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submission_reception_exception_handling" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submission reception receipt confirmation",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submission_reception_receipt_confirmation" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submission risk",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submission_risk" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submission mitigation",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submission_mitigation" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Information package file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "information_package_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submission information package file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submission_information_package_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Archival information package file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_information_package_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Dissemination information package file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "dissemination_information_package_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Submit description file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "submit_description_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Content type specification file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "content_type_specification_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Archival description file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_description_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Authority information file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "authority_information_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Preservation description file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "preservation_description_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "IP event description file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "ip_event_description_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Mimetypes definition file",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "mimetypes_definition_file" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Preservation organization receiver email",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "preservation_organization_receiver_email" # Responds to specification data
            }, {
                "hideExpression": "true",
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Preservation organization receiver url",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "preservation_organization_receiver_url" # Responds to specification data
            }
        ],
        'specification': {},
        'specification_data': {
            "archivist_organization": "National Archive xx",
            "archival_institution": "Riksarkivet",
            "archival_type": "document",
            "archival_location": "sweden-stockholm-nacka",
            "archive_policy": "archive policy 1",
            "container_format":	"tar",
            "container_format_compression": "none",
            "checksum_algorithm": "MD5",
            "submission_reception_validation": "yes",
            "submission_reception_exception_handling": "none",
            "submission_reception_receipt_confirmation": "none",
            "submission_risk": "none",
            "submission_mitigation": "none",
            "information_package_file": "ip.xml",
            "submission_information_package_file": "sip.xml",
            "archival_information_package_file": "aip.xml",
            "dissemination_information_package_file": "dip.xml",
            "submit_description_file": "info.xml", # ip_uuid
            "content_type_specification_file": "erms.xml", # siard.xml etc
            "archival_description_file": "ead.xml",
            "authority_information_file": "eac_cpf.xml",
            "preservation_description_file": "premis.xml",
            "ip_event_description_file": "ipevents.xml",
            "mimetypes_definition_file": "mime.types",
            "preservation_organization_receiver_email": "receiver@archive.xxx",
            "preservation_organization_receiver_url": "https://eta-demo.essarch.org,reta,reta",
        },
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

def installProfileAuthorityInformation(): # Profile Authority Information

    # create profile authority information dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440004',
        'name': 'Authority Information 1',
        'profile_type': 'authority_information',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Authority Information 1',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    print 'Installed profile authority information'

    return 0

def installProfileArchivalDescription(): # Profile Archival Description

    # create profile authority information dictionaries

    dct = {
        'id': '550e8400-e29b-41d4a716-446655440104',
        'name': 'Archival Description 1',
        'profile_type': 'archival_description',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Archival Description 1',
        'specification': {},
        'specification_data': {},
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

    print 'Installed profile archival description'

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
                    "label": "Start Date"
                },
                "type": "datepicker",
                "key": "startdate"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "End Date"
                },
                "type": "datepicker",
                "key": "enddate"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "disabled": True,
                    "label": "Archivist Organization"
                },
                "type": "input",
                "key": "_IP_ARCHIVIST_ORGANIZATION"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Creator"
                },
                "type": "input",
                "key": "creator"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Submitter Organization"
                },
                "type": "input",
                "key": "submitter_organization"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Submitter Individual"
                },
                "type": "input",
                "key": "submitter_individual"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Producer Organization"
                },
                "type": "input",
                "key": "producer_organization"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Producer Individual"
                },
                "type": "input",
                "key": "producer_individual"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "IP Owner"
                },
                "type": "input",
                "key": "ipowner"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Preservation Organization"
                },
                "type": "input",
                "key": "preservation_organization"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "System Name"
                },
                "type": "input",
                "key": "systemname"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "System Version"
                },
                "type": "input",
                "key": "systemversion"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "System Type"
                },
                "type": "input",
                "key": "systemtype"
            },
        ],
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/SDTemplate.json')).read()),
        'specification_data': {
            "profile": "my profile",
            "startdate": "2016-11-10",
            "enddate": "2016-12-20",
            "creator": "the creator",
            "submitter_organization": "the submitter organization",
            "submitter_individual": "the submitter individual",
            "producer_organization": "the submitter organization",
            "producer_individual": "the producer individual",
            "ipowner": "the ip owner",
            "preservation_organization": "the preservation organization",
            "systemname": "the system name",
            "systemversion": "the system version",
            "systemtype": "the system type",
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
                                "children": [
                                    {
                                        "use": "content",
                                        "type": "file",
                                        "name": "content"
                                    }
                                ]
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
                    "label": "Type"
                },
                "type": "input",
                "key": "mets_type"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "disabled": True,
                    "label": "Archivist Organization"
                },
                "type": "input",
                "key": "_IP_ARCHIVIST_ORGANIZATION"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist Organization Note"
                },
                "type": "input",
                "key": "archivist_organization_note"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Organization"
                },
                "type": "input",
                "key": "creator_organization_name"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Organization Note"
                },
                "type": "input",
                "key": "creator_organization_note"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist Software"
                },
                "type": "input",
                "key": "archivist_software_name"
            },
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist Software Note"
                },
                "type": "input",
                "key": "archivist_software_note"
            },
        ],
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/JSONTemplate.json')).read()),
        'specification_data': {
            "mets_type": "Personnel",
            "archivist_organization_note": "Archivist Organization 1 Note",
            "creator_organization_name": "Creator Organization 1",
            "creator_organization_note": "Creator Organization 1 Note",
            "archivist_software_name": "Archivist Software 1",
            "archivist_software_note": "Archivist Software 1 Note",
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

    dct3 = {
        'id': '550e8400-e29b-41d4a716-446655440018',
        'name': 'Sydarkivera',
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
                "use": "mets_file",
                "type": "file",
                "name": "mets.xml"
            },
            {
                "type": "folder",
                "name": "metadata",
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
                "name": "content",
                "children": [
                    {
                        "use": "content",
                        "type": "file",
                        "name": "content"
                    }
                ]
            },
            {
                "use": "preservation_description_file",
                "type": "file",
                "name": "premis.xml"
            }
        ],
        'template': [
            {
                "key": "content_type",
                "type": "select",
                "templateOptions": {
                    "label": "Content Type",
                    "options": [
                        {
                          "name": "Electronic Record Management System",
                          "value": "ERMS"
                        },
                        {
                          "name": "Personnel system",
                          "value": "Personnel"
                        },
                        {
                          "name": "Medical record(s)",
                          "value": "Medical record"
                        },
                        {
                          "name": "Economics",
                          "value": "Economics systems"
                        },
                        {
                          "name": "Databases",
                          "value": "Databases"
                        },
                        {
                          "name": "Webpages",
                          "value": "Webpages"
                        },
                        {
                          "name": "Geografical Information Systems",
                          "value": "GIS"
                        },
                        {
                          "name": "No specification",
                          "value": "No specification"
                        },
                        {
                          "name": "Archival Information Collection",
                          "value": "AIC"
                        },
                        {
                          "name": "Archival Information",
                          "value": "Archival Information"
                        },
                        {
                          "name": "Unstructured",
                          "value": "Unstructured"
                        },
                        {
                          "name": "Single records",
                          "value": "Single records"
                        },
                        {
                          "name": "Publication",
                          "value": "Publication"
                        },
                    ]
                },
            },
            {
                "templateOptions": {
                    "type": "text",
                    "disabled": True,
                    "label": "Submission Agreement"
                },
                "type": "input",
                "key": "_SA_NAME"
            },
            {
                "key": "access_restrict",
                "type": "select",
                "templateOptions": {
                    "label": "Access Restrict",
                    "options": [
                        {
                          "name": "Secrecy",
                          "value": "Secrecy"
                        },
                        {
                          "name": "PuL",
                          "value": "PuL"
                        },
                        {
                          "name": "Secrecy and PuL",
                          "value": "Secrecy and PuL"
                        },
                    ]
                },
            },
            {
                "key": "_IP_ARCHIVIST_ORGANIZATION",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "disabled": True,
                    "label": "Archivist Organization"
                },
            },
            {
                "key": "archivist_organization_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist Organization Note"
                },
            },
            {
                "key": "archivist_software",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist Software"
                },
            },
            {
                "key": "archivist_software_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist Software Note"
                },
            },
            {
                "key": "creator_organization",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Organization"
                },
            },
            {
                "key": "creator_organization_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Organization Note"
                },
            },
            {
                "key": "creator_software",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Software"
                },
            },
            {
                "key": "creator_software_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Software Note"
                },
            },
            {
                "key": "data_submission_session",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Data Submission Session"
                },
            },
            {
                "key": "package_number",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Package Number"
                },
            },
            {
                "key": "record_status",
                "type": "select",
                "defaultValue": "NEW",
                "templateOptions": {
                    "label": "Record Status",
                    "options": [
                        {
                          "name": "SUPPLEMENT",
                          "value": "SUPPLEMENT"
                        },
                        {
                          "name": "REPLACEMENT",
                          "value": "REPLACEMENT"
                        },
                        {
                            "name": "NEW",
                            "value": "NEW"
                        },
                        {
                          "name": "TEST",
                          "value": "TEST"
                        },
                        {
                          "name": "VERSION",
                          "value": "VERSION"
                        },
                        {
                          "name": "OTHER",
                          "value": "OTHER"
                        },
                    ]
                },
            },
            {
                "key": "reference_code",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Reference Code"
                },
            },
            {
                "key": "producer_organization",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Producer Organization"
                },
            },
            {
                "key": "producer_organization_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Producer Organization Note"
                },
            },
            {
                "key": "system_type",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "System Type"
                },
            },
            {
                "key": "appraisal",
                "type": "select",
                "templateOptions": {
                    "label": "Appraisal",
                    "options": [
                        {
                          "name": "Yes",
                          "value": "Yes"
                        },
                        {
                          "name": "No",
                          "value": "No"
                        },
                    ]
                },
            },
            {
                "key": "content_type_specification",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Content Type Specification"
                },
            },
            {
                "key": "agreement_form",
                "type": "select",
                "templateOptions": {
                    "label": "Agreement Form",
                    "options": [
                        {
                          "name": "AGREEMENT",
                          "value": "AGREEMENT"
                        },
                        {
                          "name": "DEPOSIT",
                          "value": "DEPOSIT"
                        },
                        {
                          "name": "GIFT",
                          "value": "GIFT"
                        },
                        {
                          "name": "Not specified",
                          "value": "Not specified"
                        },
                    ]
                },
            },
            {
                "key": "previous_submission_agreement",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Previous Submission Agreement"
                },
            },
            {
                "key": "previous_reference_code",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Previous Reference Code",
                },
            },
            {
                "key": "start_date",
                "type": "datepicker",
                "templateOptions": {
                    "type": "text",
                    "label": "Start Date"
                },
            },
            {
                "key": "end_date",
                "type": "datepicker",
                "templateOptions": {
                    "type": "text",
                    "label": "End Date"
                },
            },
            {
                "key": "information_class",
                "type": "select",
                "templateOptions": {
                    "label": "Information Class",
                    "options": [
                        {
                          "name": "Klass 1 (måttlig)",
                          "value": "Klass 1"
                        },
                        {
                          "name": "Klass 2 (kännbar)",
                          "value": "Klass 2"
                        },
                        {
                          "name": "Klass 3 (allvarlig)",
                          "value": "Klass 3"
                        },
                        {
                          "name": "Klass 4 (rikets säkerhet)",
                          "value": "Klass 4"
                        },
                    ]
                },
            },
            {
                "key": "editor_organization",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Editor Organization"
                },
            },
            {
                "key": "editor_organization_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Editor Organization Note"
                },
            },
            {
                "key": "preservation_organization",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Preservation Organization"
                },
            },
            {
                "key": "preservation_organization_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Preservation Organization Note"
                },
            },
            {
                "key": "creator_individual",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Individual"
                },
            },
            {
                "key": "creator_individual_note",
                "type": "input",
                "templateOptions": {
                    "type": "text",
                    "label": "Creator Individual Note"
                },
            },
        ],
        'specification': json.loads(open(os.path.join(
            settings.BASE_DIR,
            'templates/SydarkiveraSIPTemplate.json'
        )).read()),
        'specification_data': {}
    }

    # create according to model with many fields
    Profile.objects.create(**dct)
    Profile.objects.create(**dct2)
    Profile.objects.create(**dct3)

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
            'responsible': User.objects.get_or_create(
                username='Freddie Mercury'
            )[0],
        },
        {
            'label': 'Arkiv 2',
            'responsible': User.objects.get_or_create(
                username='Roger Taylor'
            )[0],
        },
        {
            'label': 'Arkiv 3',
            'responsible': User.objects.get_or_create(
                username='Brian May'
            )[0],
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
