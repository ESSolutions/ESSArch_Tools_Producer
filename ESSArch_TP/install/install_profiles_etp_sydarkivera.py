#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-

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

import json
import os

import django
django.setup()

from django.conf import settings

from ESSArch_Core.profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileSA,
)


def installProfiles():
    sa = installSubmissionAgreement()

    installProfileTransferProject(sa)
    installProfileContentType(sa)
    installProfileDataSelection(sa)
    installProfileAuthorityInformation(sa)
    installProfileArchivalDescription(sa)
    installProfileImport(sa)
    installProfileSubmitDescription(sa)
    installProfileSIP(sa)
    installProfileAIP(sa)
    installProfileDIP(sa)
    installProfileWorkflow(sa)
    installProfilePreservationMetadata(sa)

    return 0

def installSubmissionAgreement():

    # create submission agreement dictionaries
    dct = {
	  'sa_name': 'SA Sydarkivera and Organization x',
	  'sa_type': 'Standard',
	  'sa_status': 'Agreed',
	  'sa_label': 'Submission Agreement Sydarkivera and Organization x',
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

    sa, _ = SubmissionAgreement.objects.get_or_create(sa_name=dct['sa_name'], defaults=dct)

    print 'Installed submission agreement'

    return sa

def installProfileTransferProject(sa):

    dct = {
        'name': 'Transfer Project Profile 1',
        'profile_type': 'transfer_project',
        'type': 'Implementation',
        'status': 'Agreed',
        'label': 'Transfer Project Profile 1',
        'schemas': {},
        'template': [
            {
                "templateOptions": {
                    "type": "text",
                    "label": "Archival institution",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_institution"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "Archivist organization",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archivist_organization"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "Archival type",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_type"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "Archival location",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archival_location"
            }, {
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Archive Policy",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "archive_policy"
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
                "templateOptions": {
                    "disabled": True,
                    "type": "text",
                    "label": "Container format compression",
                    "desc": "xxx",
                },
                "type": "input",
                "key": "container_format_compression"
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
                "templateOptions": {
                    "type": "text",
                    "label": "Preservation organization receiver email",
                },
                "type": "input",
                "key": "preservation_organization_receiver_email"
            }, {
                "templateOptions": {
                    "type": "text",
                    "label": "Preservation organization receiver url",
                },
                "type": "input",
                "key": "preservation_organization_receiver_url"
            }
        ],
        'specification': {},
        'specification_data': {
            "archivist_organization": "Organization xx",
            "archival_institution": "Sydarkivera",
            "archival_type": "document",
            "archival_location": "Växjö",
            "archive_policy": "Archive policy 1",
            "container_format":	"tar",
            "checksum_algorithm": "MD5",
            "preservation_organization_receiver_email": "bjorn@essolutions.se",
            "preservation_organization_receiver_url": "https://eta-demo.essarch.org,reta,reta",
        },
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)
    ProfileSA.objects.get_or_create(profile=profile, submission_agreement=sa)

    print 'Installed profile transfer project'

    return 0


def installProfileSubmitDescription(sa):

    dct = {
        'name': 'Submit description of a single SIP',
        'profile_type': 'submit_description',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Submit description of a single SIP',
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
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/Sydarkivera_SD_Template.json')).read()),
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

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)
    ProfileSA.objects.get_or_create(profile=profile, submission_agreement=sa)

    print 'Installed profile submit description'

    return 0


def installProfileSIP(sa):

    dct = {
        'name': 'SIP Sydarkivera',
        'profile_type': 'sip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'SIP profile for Sydarkivera submissions',
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
                    },
                    {
                        "use": "preservation_description_file",
                        "type": "file",
                        "name": "premis.xml"
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
            }
        ],
        'template': [
            {
                "key": "content_type",
                "type": "select",
                "templateOptions": {
                    "required": True,
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
                    "required": True,
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
                    "required": True,
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
                    "required": True,
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
                    "required": True,
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
                    "required": True,
                    "type": "text",
                    "label": "Data Submission Session"
                },
            },
            {
                "key": "package_number",
                "type": "input",
                "templateOptions": {
                    "required": True,
                    "type": "text",
                    "label": "Package Number"
                },
            },
            {
                "key": "record_status",
                "type": "select",
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
                    "required": True,
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
                    "required": True,
                    "type": "text",
                    "label": "System Type"
                },
            },
            {
                "key": "appraisal",
                "type": "select",
                "templateOptions": {
                    "required": True,
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
                    "required": True,
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
                    "required": True,
                    "type": "text",
                    "label": "Start Date"
                },
            },
            {
                "key": "end_date",
                "type": "datepicker",
                "templateOptions": {
                    "required": True,
                    "type": "text",
                    "label": "End Date"
                },
            },
            {
                "key": "information_class",
                "type": "select",
                "templateOptions": {
                    "required": True,
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
                    "required": True,
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
                    "required": True,
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
                    "required": True,
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
        'specification': json.loads(open(os.path.join(settings.BASE_DIR,'templates/Sydarkivera_SIP_Template.json')).read()),
        'specification_data': {
            "content_type": "Personnel",
            "record_status": "NEW",
            "access_restrict": "Secrecy",
        }
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)
    ProfileSA.objects.get_or_create(profile=profile, submission_agreement=sa)

    print 'Installed profile SIP'

    return 0


def installProfileAIP(sa):

    dct = {
        'name': 'AIP Sydarkivera',
        'profile_type': 'aip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'AIP profile for Sydarkivera Packages',
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

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile AIP'

    return 0


def installProfileDIP(sa):

    dct = {
        'name': 'DIP Sydarkivera',
        'profile_type': 'dip',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'DIP profile for Sydarkivera Packages',
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

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile DIP'

    return 0


def installProfileContentType(sa):

    dct = {
        'name': 'SE ERMS',
        'profile_type': 'content_type',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Content based on SE ERMS specification',
        'specification': {},
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile content type'

    return 0


def installProfileAuthorityInformation(sa):

    dct = {
        'name': 'Authority Information 1',
        'profile_type': 'authority_information',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Authority Information 1',
        'specification': {},
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile authority information'

    return 0

def installProfileArchivalDescription(sa):

    dct = {
        'name': 'Archival Description 1',
        'profile_type': 'archival_description',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Archival Description 1',
        'specification': {},
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile archival description'

    return 0


def installProfilePreservationMetadata(sa):

    dct = {
        'name': 'Preservation profile xx',
        'profile_type': 'preservation_metadata',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Preservation profile for AIP xxyy',
        'specification': json.loads(open(os.path.join(settings.BASE_DIR, 'templates/Premis_Template.json')).read()),
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile preservation metadata'

    return 0


def installProfileDataSelection(sa):

    dct = {
        'name': 'Data selection of business system xx',
        'profile_type': 'data_selection',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Data selection of business system xx',
        'specification': {},
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile data selection'

    return 0


def installProfileImport(sa):

    dct = {
        'name': 'Transformation import profile for system xx',
        'profile_type': 'import',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Transformation from system x to specification y',
        'specification': {},
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile import'

    return 0


def installProfileWorkflow(sa):

    dct = {
        'name': 'Workflow xx for Pre-Ingest',
        'profile_type': 'workflow',
        'type': 'Implementation',
        'status': 'Draft',
        'label': 'Workflow Create SIP for Pre-Ingest',
        'specification': {},
        'specification_data': {},
    }

    profile, _ = Profile.objects.update_or_create(name=dct['name'], defaults=dct)

    print 'Installed profile workflow'

    return 0


if __name__ == '__main__':
    installProfiles()
