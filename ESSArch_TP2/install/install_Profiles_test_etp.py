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

# own models etc
from configuration.models import (
    EventType
)

from ip.models import (
    EventIP,
    InformationPackage,
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
)

from preingest.models import (
    ProcessStep,
    ProcessTask,
)

from profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileRel,
)

# settings
site_profile = "SE" # SE_NEW, SE, NO, EC
#zone = "zone1" # ETP=zone1, ETA=zone2


def installProfiles(): # Install all different profiles
    # First remove all existing data
    EventIP.objects.all().delete()
    EventType.objects.all().delete()
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
    installEventTypes()                         # Event Types
    installEventIPs()                           # Events

    return 0


def installWorkflows():
    installSteps()                              # Steps
    installTasks()                              # Tasks


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

    ProfileRel.objects.bulk_create([
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440001"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440002"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440003"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440004"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440005"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440006"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440007"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440008"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440009"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440010"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440011"
            ),
            submissionagreement=sa,
            status=2
        ),
        ProfileRel(
            profile=Profile.objects.get(
                id="550e8400-e29b-41d4a716-446655440012"
            ),
            submissionagreement=sa,
            status=2
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
            "mets": {
                "dmdSec": {
                    "mdWrap": {
                        "-max": 1,
                        "xmlData": {
                            "-max": 1,
                            "-attr": [],
                            "-min": 0
                        },
                        "binData": {
                            "-max": 1,
                            "#content": [],
                            "-attr": [],
                            "-min": 0
                        },
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "MDTYPE",
                            "#content": [],
                            "-req": 1
                        }, {
                            "-name": "OTHERMDTYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "MDTYPEVERSION",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "MIMETYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "SIZE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "CREATED",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "CHECKSUM",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "CHECKSUMTYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "LABEL",
                            "#content": [],
                            "-req": 0
                        }],
                        "-min": 0
                    },
                    "-max": -1,
                    "mdRef": {
                        "-max": 1,
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "LOCTYPE",
                            "#content": [],
                            "-req": 1
                        }, {
                            "-name": "OTHERLOCTYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "MDTYPE",
                            "#content": [],
                            "-req": 1
                        }, {
                            "-name": "OTHERMDTYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "MDTYPEVERSION",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "MIMETYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "SIZE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "CREATED",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "CHECKSUM",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "CHECKSUMTYPE",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "LABEL",
                            "#content": [],
                            "-req": 0
                        }, {
                            "-name": "XPTR",
                            "#content": [],
                            "-req": 0
                        }],
                        "-min": 0
                    },
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 1
                    }, {
                        "-name": "GROUPID",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "ADMID",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "CREATED",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "STATUS",
                        "#content": [],
                        "-req": 0
                    }],
                    "-min": 0
                },
                "-attr": [{
                    "-name": "ID",
                    "#content": [{
                        "var": "ID"
                    }],
                    "-req": 0
                }, {
                    "-name": "OBJID",
                    "#content": [
                        {
                        "var": "OBJID"
                        }, {
                            "text": "asd"
                        }
                    ],
                    "-req": 1
                }, {
                    "-name": "LABEL",
                    "#content": [
                        {
                            "var": "LABEL"
                        }
                    ],
                    "-req": 0
                }, {
                    "-name": "TYPE",
                    "#content": [
                        {
                            "text": "Medical record"
                        }
                    ],
                    "-req": 1
                }, {
                    "-name": "PROFILE",
                    "#content": [
                        {
                            "var": "PROFILE"
                        }
                    ],
                    "-req": 1
                }],
                "metsHdr": {
                    "-max": 1,
                    "metsDocumentID": {
                        "-max": 1,
                        "#content": [],
                        "-attr": [],
                        "-min": 0
                    },
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "ADMID",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "CREATEDATE",
                        "#content": [],
                        "-req": 1
                    }, {
                        "-name": "LASTMODDATE",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "RECORDSTATUS",
                        "#content": [],
                        "-req": 0
                    }],
                    "altRecordID": {
                        "-max": -1,
                        "#content": [],
                        "-attr": [],
                        "-min": 1
                    },
                    "agent": [{
                        "note": {
                            "-max": -1,
                            "#content": [],
                            "-attr": [],
                            "-min": 0
                        },
                        "-max": -1,
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                        "-name": "ROLE",
                        "#content": [],
                        "-req": 1
                        }, {
                        "-name": "OTHERROLE",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "TYPE",
                        "#content": [],
                        "-req": 1
                        }, {
                        "-name": "OTHERTYPE",
                        "#content": [],
                        "-req": 0
                        }],
                        "name": {
                            "-max": 1,
                            "#content": [],
                            "-attr": [],
                            "-min": 0
                        },
                        "-min": 3
                    }, {
                    "note": {
                        "-max": -1,
                        "#content": [],
                        "-attr": [],
                        "-min": 0
                    },
                    "-max": -1,
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "ROLE",
                        "#content": [],
                        "-req": 1
                    }, {
                        "-name": "OTHERROLE",
                        "#content": [],
                        "-req": 0
                    }, {
                        "-name": "TYPE",
                        "#content": [],
                        "-req": 1
                    }, {
                        "-name": "OTHERTYPE",
                        "#content": [],
                        "-req": 0
                    }],
                    "name": {
                        "-max": 1,
                        "#content": [],
                        "-attr": [],
                        "-min": 0
                    },
                    "-min": 3
                    }, {
                    "note": {
                        "-max": -1,
                        "#content": [],
                        "-attr": [],
                        "-min": 0
                    },
                    "-max": -1,
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }, {
                    "-name": "ROLE",
                    "#content": [],
                    "-req": 1
                    }, {
                    "-name": "OTHERROLE",
                    "#content": [],
                    "-req": 0
                    }, {
                    "-name": "TYPE",
                    "#content": [],
                    "-req": 1
                    }, {
                    "-name": "OTHERTYPE",
                    "#content": [],
                    "-req": 0
                    }],
                    "name": {
                        "-max": 1,
                        "#content": [],
                        "-attr": [],
                        "-min": 0
                    },
                    "-min": 3
                    }],
                    "-min": 0
                },
                "amdSec": {
                    "-max": -1,
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 1
                    }],
                    "rightsMD": {
                        "-max": -1,
                        "-attr": [],
                        "-min": 0
                    },
                    "-min": 0,
                    "sourceMD": {
                        "-max": -1,
                        "-attr": [],
                        "-min": 0
                    },
                    "techMD": {
                        "-max": -1,
                        "-attr": [],
                        "-min": 0
                    },
                    "digiprovMD": {
                        "-max": -1,
                        "-attr": [],
                        "-min": 0
                    }
                },
                "behaviorSec": {
                    "-max": -1,
                    "behaviorSec": {
                        "-max": -1,
                        "-attr": [],
                        "-min": 0
                    },
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }, {
                    "-name": "CREATED",
                    "#content": [],
                    "-req": 0
                    }, {
                    "-name": "LABEL",
                    "#content": [],
                    "-req": 0
                    }],
                    "behavior": {
                        "-max": -1,
                        "interfaceDef": {
                            "-max": 1,
                            "-attr": [{
                                "-name": "ID",
                                "#content": [],
                                "-req": 0
                            }, {
                            "-name": "LABEL",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "LOCTYPE",
                            "#content": [],
                            "-req": 1
                            }, {
                            "-name": "OTHERLOCTYPE",
                            "#content": [],
                            "-req": 0
                            }],
                            "-min": 0
                        },
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                        "-name": "STRUCTID",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "BTYPE",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "CREATED",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "LABEL",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "GROUPID",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "ADMID",
                        "#content": [],
                        "-req": 0
                        }],
                        "mechanism": {
                            "-max": 1,
                            "-attr": [],
                            "-min": 0
                        },
                        "-min": 0
                    },
                    "-min": 0
                },
                "structLink": {
                    "smLinkGrp": {
                        "-max": 1,
                        "smArcLink": {
                            "-max": -1,
                            "-attr": [{
                                "-name": "ID",
                                "#content": [],
                                "-req": 0
                            }, {
                            "-name": "ARCTYPE",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "ADMID",
                            "#content": [],
                            "-req": 0
                            }],
                            "-min": 1
                        },
                        "smLocatorLink": [{
                            "-max": -1,
                            "-attr": [{
                                "-name": "ID",
                                "#content": [],
                                "-req": 0
                            }],
                            "-min": 2
                        }, {
                        "-max": -1,
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }],
                        "-min": 2
                        }],
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                        "-name": "ARCLINKORDER",
                        "#content": [],
                        "-req": 0
                        }],
                        "-min": 0
                    },
                    "-max": 1,
                    "smLink": {
                        "-max": 1,
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }],
                        "-min": 0
                    },
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }],
                    "-min": 0
                },
                "fileSec": {
                    "-max": 1,
                    "fileGrp": {
                        "-max": -1,
                        "fileGrp": {
                            "-max": -1,
                            "-attr": [],
                            "-min": 0
                        },
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                        "-name": "VERSDATE",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "ADMID",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "USE",
                        "#content": [],
                        "-req": 0
                        }],
                        "file": {
                            "-max": -1,
                            "-attr": [{
                                "-name": "ID",
                                "#content": [],
                                "-req": 1
                            }, {
                            "-name": "SEQ",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "MIMETYPE",
                            "#content": [],
                            "-req": 1
                            }, {
                            "-name": "SIZE",
                            "#content": [],
                            "-req": 1
                            }, {
                            "-name": "CREATED",
                            "#content": [],
                            "-req": 1
                            }, {
                            "-name": "CHECKSUM",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "CHECKSUMTYPE",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "OWNERID",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "ADMID",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "DMDID",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "GROUPID",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "USE",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "BEGIN",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "END",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "BETYPE",
                            "#content": [],
                            "-req": 0
                            }],
                            "stream": {
                                "-max": -1,
                                "-attr": [],
                                "-min": 0
                            },
                            "FLocat": {
                                "-max": 1,
                                "-attr": [{
                                    "-name": "ID",
                                    "#content": [],
                                    "-req": 0
                                }, {
                                "-name": "LOCTYPE",
                                "#content": [],
                                "-req": 1
                                }, {
                                "-name": "OTHERLOCTYPE",
                                "#content": [],
                                "-req": 0
                                }, {
                                "-name": "USE",
                                "#content": [],
                                "-req": 0
                                }],
                                "-min": 0
                            },
                            "-min": 0,
                            "FContent": {
                                "-max": 1,
                                "xmlData": {
                                    "-max": 1,
                                    "-attr": [],
                                    "-min": 0
                                },
                                "binData": {
                                    "-max": 1,
                                    "#content": [],
                                    "-attr": [],
                                    "-min": 0
                                },
                                "-attr": [{
                                    "-name": "ID",
                                    "#content": [],
                                    "-req": 0
                                }, {
                                "-name": "USE",
                                "#content": [],
                                "-req": 0
                                }],
                                "-min": 0
                            },
                            "transformFile": {
                                "-max": -1,
                                "-attr": [],
                                "-min": 0
                            },
                            "file": {
                                "-max": -1,
                                "-attr": [],
                                "-min": 0
                            }
                        },
                        "-min": 0
                    },
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }],
                    "-min": 0
                },
                "structMap": {
                    "-max": -1,
                    "div": {
                        "fptr": {
                            "-max": -1,
                            "par": {
                                "-max": 1,
                                "area": {
                                    "-max": 1,
                                    "-attr": [{
                                        "-name": "ID",
                                        "#content": [],
                                        "-req": 0
                                    }, {
                                    "-name": "FILEID",
                                    "#content": [],
                                    "-req": 1
                                    }, {
                                    "-name": "SHAPE",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "COORDS",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "BEGIN",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "END",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "BETYPE",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "EXTENT",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "EXTTYPE",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "ADMID",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "CONTENTIDS",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "ORDER",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "ORDERLABEL",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "LABEL",
                                    "#content": [],
                                    "-req": 0
                                    }],
                                    "-min": 0
                                },
                                "-attr": [{
                                    "-name": "ID",
                                    "#content": [],
                                    "-req": 0
                                }, {
                                "-name": "ORDER",
                                "#content": [],
                                "-req": 0
                                }, {
                                "-name": "ORDERLABEL",
                                "#content": [],
                                "-req": 0
                                }, {
                                "-name": "LABEL",
                                "#content": [],
                                "-req": 0
                                }],
                                "seq": {
                                    "-max": 1,
                                    "par": {
                                        "-max": 1,
                                        "-attr": [],
                                        "-min": 0
                                    },
                                    "area": {
                                        "-max": 1,
                                        "-attr": [],
                                        "-min": 0
                                    },
                                    "-attr": [{
                                        "-name": "ID",
                                        "#content": [],
                                        "-req": 0
                                    }, {
                                    "-name": "ORDER",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "ORDERLABEL",
                                    "#content": [],
                                    "-req": 0
                                    }, {
                                    "-name": "LABEL",
                                    "#content": [],
                                    "-req": 0
                                    }],
                                    "-min": 0
                                },
                                "-min": 0
                            },
                            "-attr": [{
                                "-name": "ID",
                                "#content": [],
                                "-req": 0
                            }, {
                            "-name": "FILEID",
                            "#content": [],
                            "-req": 1
                            }, {
                            "-name": "CONTENTIDS",
                            "#content": [],
                            "-req": 0
                            }],
                            "seq": {
                                "-max": 1,
                                "-attr": [],
                                "-min": 0
                            },
                            "area": {
                                "-max": 1,
                                "-attr": [],
                                "-min": 0
                            },
                            "-min": 0
                        },
                        "-max": 1,
                        "-attr": [{
                            "-name": "ID",
                            "#content": [],
                            "-req": 0
                        }, {
                        "-name": "ORDER",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "ORDERLABEL",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "LABEL",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "DMDID",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "ADMID",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "TYPE",
                        "#content": [],
                        "-req": 0
                        }, {
                        "-name": "CONTENTIDS",
                        "#content": [],
                        "-req": 0
                        }],
                        "-min": 0,
                        "div": {
                            "-max": -1,
                            "-attr": [],
                            "-min": 0
                        },
                        "mptr": {
                            "-max": -1,
                            "-attr": [{
                                "-name": "ID",
                                "#content": [],
                                "-req": 0
                            }, {
                            "-name": "LOCTYPE",
                            "#content": [],
                            "-req": 1
                            }, {
                            "-name": "OTHERLOCTYPE",
                            "#content": [],
                            "-req": 0
                            }, {
                            "-name": "CONTENTIDS",
                            "#content": [],
                            "-req": 0
                            }],
                            "-min": 0
                        }
                    },
                    "-attr": [{
                        "-name": "ID",
                        "#content": [],
                        "-req": 0
                    }, {
                    "-name": "TYPE",
                    "#content": [],
                    "-req": 0
                    }, {
                    "-name": "LABEL",
                    "#content": [],
                    "-req": 0
                    }],
                    "-min": 0
                }
            }
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
        'name': 'SIP based on SE FGS Package',
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
        'structure': {
            'representations': {
                'documentation': {}
            },
            'rep01': {},
            'metadata': {}
        },
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
    }

    # create according to model with many fields
    Profile.objects.create(**dct)

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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
        'specification': 'Any specification wrapped',
        'specification_data': 'Any specification data wrapped',
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
            'id': '25d58fe1-d5c9-40d1-92de-9707de9d9ad1',
            'Label': 'Arkiv 1',
            'Content': 'ERMS',
            'Responsible': 'Freddie Mercury',
            'CreateDate': '2012-04-26T10:45:12.865096Z',
            'State': 'hmm',
            'ObjectSize': '123',
            'ObjectNumItems': '10',
            'ObjectPath': '/path1',
            'Startdate': '2011-01-01T10:45:12.865096Z',
            'Enddate': '2011-12-31T10:45:12.865096Z',
            'OAIStype': 'SIP',
            'SubmissionAgreement': SubmissionAgreement.objects.get(
                pk="550e8400-e29b-41d4a716-446655440000"
            ),
            'ArchivalInstitution': ArchivalInstitution.objects.get(
                pk="aa8e20d9-8794-4f26-9859-c3341a31f111"
            ),
            'ArchivistOrganization': ArchivistOrganization.objects.get(
                pk="2fe86f14-9b09-46e3-b272-a6e971b9d4e1"
            ),
            'ArchivalType': ArchivalType.objects.get(
                pk="fc3f23aa-203c-4aee-bb20-92373a5eba81"
            ),
            'ArchivalLocation': ArchivalLocation.objects.get(
                pk="83f1f65d-7be0-4577-ade9-543c815417b1"
            ),
        },
        {
            'id': '25d58fe1-d5c9-40d1-92de-9707de9d9ad2',
            'Label': 'Arkiv 2',
            'Content': 'Personnel',
            'Responsible': 'Roger Taylor',
            'CreateDate': '2013-05-18T12:12:12.865096Z',
            'State': 'hmm',
            'ObjectSize': '456',
            'ObjectNumItems': '20',
            'ObjectPath': '/path2',
            'Startdate': '2012-01-01T23:21:22.865096Z',
            'Enddate': '2012-08-12T01:23:21.865096Z',
            'OAIStype': 'SIP',
            'SubmissionAgreement': SubmissionAgreement.objects.get(
                pk="550e8400-e29b-41d4a716-446655440000"
            ),
            'ArchivalInstitution': ArchivalInstitution.objects.get(
                pk="aa8e20d9-8794-4f26-9859-c3341a31f112"
            ),
            'ArchivistOrganization': ArchivistOrganization.objects.get(
                pk="2fe86f14-9b09-46e3-b272-a6e971b9d4e2"
            ),
            'ArchivalType': ArchivalType.objects.get(
                pk="fc3f23aa-203c-4aee-bb20-92373a5eba82"
            ),
            'ArchivalLocation': ArchivalLocation.objects.get(
                pk="83f1f65d-7be0-4577-ade9-543c815417b2"
            ),
        },
        {
            'id': '25d58fe1-d5c9-40d1-92de-9707de9d9ad3',
            'Label': 'Arkiv 3',
            'Content': 'SFBS',
            'Responsible': 'Brian May',
            'CreateDate': '2014-01-20T09:39:15.865096Z',
            'State': 'hmm',
            'ObjectSize': '789',
            'ObjectNumItems': '30',
            'ObjectPath': '/path3',
            'Startdate': '2013-02-18T14:28:46.865096Z',
            'Enddate': '2013-12-21T08:03:21.865096Z',
            'OAIStype': 'SIP',
            'SubmissionAgreement': SubmissionAgreement.objects.get(
                pk="550e8400-e29b-41d4a716-446655440000"
            ),
            'ArchivalInstitution': ArchivalInstitution.objects.get(
                pk="aa8e20d9-8794-4f26-9859-c3341a31f113"
            ),
            'ArchivistOrganization': ArchivistOrganization.objects.get(
                pk="2fe86f14-9b09-46e3-b272-a6e971b9d4e3"
            ),
            'ArchivalType': ArchivalType.objects.get(
                pk="fc3f23aa-203c-4aee-bb20-92373a5eba83"
            ),
            'ArchivalLocation': ArchivalLocation.objects.get(
                pk="83f1f65d-7be0-4577-ade9-543c815417b3"
            ),
        },
    ]

    # create according to model with many fields
    for dct in lst:
        InformationPackage.objects.create(**dct)

    print 'Installed information packages'

    return 0


def installEventTypes():
    lst = [
        {
            'id': '9ddbcb6d-955a-4a4d-a462-bf52a708f8c1',
            'eventType': 1,
            'eventDetail': 'Prepare IP',
        },
        {
            'id': '9ddbcb6d-955a-4a4d-a462-bf52a708f8c2',
            'eventType': 2,
            'eventDetail': 'Generate XML',
        },
        {
            'id': '9ddbcb6d-955a-4a4d-a462-bf52a708f8c3',
            'eventType': 3,
            'eventDetail': 'Create directory strucutre',
        },
    ]

    # create according to model with many fields
    for dct in lst:
        EventType.objects.create(**dct)

    print 'Installed event types'

    return 0


def installEventIPs():
    lst = [
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c1'
            ),
            'eventDetail': 'Preparing the IP',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad1'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c2'
            ),
            'eventDetail': 'Adding files to XML',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad1'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c2'
            ),
            'eventDateTime': '',
            'eventDetail': 'Creating METS file',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad1'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c3'
            ),
            'eventDetail': 'Creating directory structure from JSON',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad1'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c1'
            ),
            'eventDetail': 'Preparing the IP',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad2'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c2'
            ),
            'eventDetail': 'Adding files to XML',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad2'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c2'
            ),
            'eventDateTime': '',
            'eventDetail': 'Creating PREMIS file',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad2'
            ),
        },
        {
            'eventType': EventType.objects.get(
                pk='9ddbcb6d-955a-4a4d-a462-bf52a708f8c3'
            ),
            'eventDetail': 'Creating directory structure from JSON',
            'eventApplication': '',
            'eventVersion': '',
            'eventOutcome': '',
            'eventOutcomeDetailNote': '',
            'linkingAgentIdentifierValue': '',
            'linkingObjectIdentifierValue': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad2'
            ),
        },
    ]

    # create according to model with many fields
    for dct in lst:
        EventIP.objects.create(**dct)

    print 'Installed events'

    return 0


def installSteps():
    lst = [
        {
            'id': '7d8efe1e-2d65-45e2-8c39-63f0609131e1',
            'name': 'Prepare IP',
            'type': 10,
            'user': 'Edsger W. Dijkstra',
            'information_package': InformationPackage.objects.get(
                pk='25d58fe1-d5c9-40d1-92de-9707de9d9ad1'
            )
        },
        {
            'id': '7d8efe1e-2d65-45e2-8c39-63f0609131e2',
            'name': 'Create directory structure',
            'type': 10,
            'user': 'Lester Randolph Ford Jr.',
        },
        {
            'id': '7d8efe1e-2d65-45e2-8c39-63f0609131e3',
            'name': 'Generate metadata',
            'type': 10,
            'user': 'Delbert Ray Fulkerson',
        },
    ]

    for dct in lst:
        if dct['id'] == '7d8efe1e-2d65-45e2-8c39-63f0609131e2':
            dct['parent_step'] = ProcessStep.objects.get(
                pk='7d8efe1e-2d65-45e2-8c39-63f0609131e1'
            )
            dct['parent_step_pos'] = 1

        if dct['id'] == '7d8efe1e-2d65-45e2-8c39-63f0609131e3':
            dct['parent_step'] = ProcessStep.objects.get(
                pk='7d8efe1e-2d65-45e2-8c39-63f0609131e1'
            )
            dct['parent_step_pos'] = 2

        ProcessStep.objects.create(**dct)

    print 'Installed steps'

    return 0


def installTasks():
    lst = [
        {
            'id': '14319c7d-f65f-40cf-b1ec-2350666136b1',
            'name': 'Create physical model',
            'params': {
                'structure': {
                    'representations': {
                        'documentation': {}
                    },
                    'rep01': {},
                    'metadata': {}
                }
            },
            'progress': 100,
            'status': 'SUCCESS',
            'processstep': ProcessStep.objects.get(
                pk='7d8efe1e-2d65-45e2-8c39-63f0609131e2'
            ),
            'processstep_pos': 1,
        },
        {
            'id': '14319c7d-f65f-40cf-b1ec-2350666136b2',
            'name': 'Generate checksums',
            'params': {
                'files': [
                    '/path/to/first/file.ext',
                    '/path/to/second/file.ext',
                    '/path/to/third/file.ext',
                ],
                'algorithm': 'sha256',
            },
            'result': [
                {
                    'file': '/path/to/first/file.ext',
                    'checksum': '688787d8ff144c502c7f5cffaafe2cc588d86079f9de88304c26b0cb99ce91c6'
                },
                {
                    'file': '/path/to/second/file.ext',
                    'checksum': 'c81ebd1b4c490ff605a7cb94561646c0c344170862e15c4f5b94721073f23a38'
                },
            ],
            'progress': 66,
            'status': 'STARTED',
            'processstep': ProcessStep.objects.get(
                pk='7d8efe1e-2d65-45e2-8c39-63f0609131e3'
            ),
            'processstep_pos': 1,
        }
    ]

    for dct in lst:
        """
        if dct['id'] == '7d8efe1e-2d65-45e2-8c39-63f0609131e2':
            dct['parent_step'] = ProcessTask.objects.get(
                pk='7d8efe1e-2d65-45e2-8c39-63f0609131e1'
            )
            dct['parent_step_pos'] = 1
        """

        ProcessTask.objects.create(**dct)
    print 'Installed tasks'

    return 0

if __name__ == '__main__':
    installProfiles()
    installIPs()
    installWorkflows()
