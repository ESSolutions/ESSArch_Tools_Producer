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
from profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileTransferProjectRel,
    ProfileContentTypeRel,
    ProfileDataSelectionRel,
    ProfileClassificationRel,
    ProfileImportRel,
    ProfileSubmitDescriptionRel,
    ProfileSIPRel,
    ProfileAIPRel,
    ProfileDIPRel,
    ProfileWorkflowRel,
    ProfilePreservationMetadataRel,
)

# settings
site_profile = "SE" # SE_NEW, SE, NO, EC
#zone = "zone1" # ETP=zone1, ETA=zone2

def installProfiles(): # Install all different profiles
    # First remove all existing data
    SubmissionAgreement.objects.all().delete()
    Profile.objects.all().delete()

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
    installSubmissionAgreement()     		# Submission Agreement

    return 0

def installSubmissionAgreement(): # Submission Agreement

    # create submission agreement dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440000',
	  'sa_name':'SA National Archive xx and Government x',
	  'sa_type':'Standard',
	  'sa_status':'Agreed',
	  'sa_label':'Submission Agreement Naxx and Government x',
	  'sa_cm_version':'1.0',
	  'sa_cm_release_date':'2012-04-26T12:45:00+01:00',
	  'sa_cm_change_authority':'Ozzy Osbourne, NAxx',
	  'sa_cm_change_description':'Original',
	  'sa_cm_sections_affected':'None',
	  'sa_producer_organization':'Government x',
	  'sa_producer_main_name':'Elton John',
	  'sa_producer_main_address':'Bourbon Street 123, City x, Country y',
	  'sa_producer_main_phone':'46 (0)8-123450',
	  'sa_producer_main_email':'Elton.John@company.se',
	  'sa_producer_main_additional':'Responsible for contract',
	  'sa_producer_individual_name':'Mike Oldfield',
	  'sa_producer_individual_role':'Archivist',
	  'sa_producer_individual_phone':'46 (0)8-123451',
	  'sa_producer_individual_email':'Mike.Oldfield@company.se',
	  'sa_producer_individual_additional':'Principal archivist',
	  'sa_archivist_organization':'National Archive xx',
	  'sa_archivist_main_name':'Ozzy Osbourne',
	  'sa_archivist_main_address':'Main street 123, City x, Country y',
	  'sa_archivist_main_phone':'46 (0)8-1001001',
	  'sa_archivist_main_email':'Ozzy.Osbourne@archive.org',
	  'sa_archivist_main_additional':'Responsible for contract',
	  'sa_archivist_individual_name':'Lita Ford',
	  'sa_archivist_individual_role':'Archivist',
	  'sa_archivist_individual_phone':'46 (0)8-1001002',
	  'sa_archivist_individual_email':'Lita.Ford@archive.org',
	  'sa_archivist_individual_additional':'Principal archivist',
	  'sa_designated_community_description':'Designated community description',
	  'sa_designated_community_individual_name':'Elvis Presley',
	  'sa_designated_community_individual_role':'Artist',
	  'sa_designated_community_individual_phone':'46 (0)8-2002001',
	  'sa_designated_community_individual_email':'Elvis.Presley@xxx.org',
	  'sa_designated_community_individual_additional':'Celebrity',
    }

    # create according to model with many fields
    sa = SubmissionAgreement.objects.create(**dct)

    ProfileTransferProjectRel.objects.create(
        profiletransferproject=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440001"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileContentTypeRel.objects.create(
        profilecontenttype=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440002"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileDataSelectionRel.objects.create(
        profiledataselection=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440003"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileClassificationRel.objects.create(
        profileclassification=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440004"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileImportRel.objects.create(
        profileimport=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440005"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileSubmitDescriptionRel.objects.create(
        profilesubmitdescription=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440006"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileSIPRel.objects.create(
        profilesip=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440007"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileAIPRel.objects.create(
        profileaip=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440008"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileDIPRel.objects.create(
        profiledip=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440009"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfileWorkflowRel.objects.create(
        profileworkflow=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440010"
        ),
        submissionagreement=sa,
        status=2
    )
    ProfilePreservationMetadataRel.objects.create(
        profilepreservationmetadata=Profile.objects.get(
            id="550e8400-e29b-41d4a716-446655440011"
        ),
        submissionagreement=sa,
        status=2
    )

    #logger.info('Installed Submission Agreement')
    print 'Installed submission agreement'

    return 0

def installProfileTransferProject(): # Profile Transfer Project

    # create profile transfer project dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440001',
	  'name':'SE ERMS Delivery',
          'profile_type': 'transfer_project',
	  'type':'Implementation',
	  'status':'Agreed',
	  'label':'Example of SIP for delivery of SE ERMS',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Transfer Project')
    print 'Installed profile transfer project'

    return 0

def installProfileContentType(): # Profile Content Type

    # create profile content type dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440002',
	  'name':'SE ERMS',
          'profile_type': 'content_type',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'Content based on SE ERMS specification',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Content Type')
    print 'Installed profile content type'

    return 0

def installProfileDataSelection(): # Profile Data Selection

    # create profile data selection dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440003',
	  'name':'Classification of business system xx',
          'profile_type': 'data_selection',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'Data selection of business system xx',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Data Selection')
    print 'Installed profile data selection'

    return 0

def installProfileClassification(): # Profile Classification

    # create profile classification dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440004',
	  'name':'Classification of archived objects',
          'profile_type': 'classification',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'Classification of archived content',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Classification')
    print 'Installed profile classification'

    return 0

def installProfileImport(): # Profile Import

    # create profile import dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440005',
	  'name':'Transformation import profile for system xx',
          'profile_type': 'import',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'Transformation from system x to specification y',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Import')
    print 'Installed profile import'

    return 0

def installProfileSubmitDescription(): # Profile Submit Description

    # create profile submit description dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440006',
	  'name':'Submit description of a single SIP',
          'profile_type': 'submit_description',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'Desription of a one2one SIP2AIP',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Submit Description')
    print 'Installed profile submit description'

    return 0

def installProfileSIP(): # Profile Submission Information Package

    # create profile submission information package dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440007',
	  'name':'SIP based on SE FGS Package',
          'profile_type': 'sip',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'SIP profile for SE submissions',
	  'representation_info':'Documentation 1',
	  'preservation_descriptive_info':'Documentation 2',
	  'supplemental':'Documentation 3',
	  'access_constraints':'Documentation 4',
	  'datamodel_reference':'Documentation 5',
	  'additional':'Documentation 6',
	  'submission_method':'Electronically',
	  'submission_schedule':'Once',
	  'submission_data_inventory':'According to submit description',
	  'structure':'SIP SE structure xx',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile SIP')
    print 'Installed profile SIP'

    return 0

def installProfileAIP(): # Profile Archival Information Package

    # create profile archival information package dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440008',
	  'name':'AIP based on SE FGS Package',
          'profile_type': 'aip',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'AIP profile for SE Packages',
	  'representation_info':'Documentation 1',
	  'preservation_descriptive_info':'Documentation 2',
	  'supplemental':'Documentation 3',
	  'access_constraints':'Documentation 4',
	  'datamodel_reference':'Documentation 5',
	  'additional':'Documentation 6',
	  'submission_method':'Electronically',
	  'submission_schedule':'Once',
	  'submission_data_inventory':'According to submit description',
	  'structure':'AIP SE structure xx',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile AIP')
    print 'Installed profile AIP'

    return 0

def installProfileDIP(): # Profile Dissemination Information Package

    # create profile dissemination information package dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440009',
	  'name':'DIP based on SE FGS Package',
          'profile_type': 'dip',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'DIP profile for SE Packages',
	  'representation_info':'Documentation 1',
	  'preservation_descriptive_info':'Documentation 2',
	  'supplemental':'Documentation 3',
	  'access_constraints':'Documentation 4',
	  'datamodel_reference':'Documentation 5',
	  'additional':'Documentation 6',
	  'submission_method':'Electronically',
	  'submission_schedule':'Once',
	  'submission_data_inventory':'According to submit description',
	  'structure':'DIP SE structure xx',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile DIP')
    print 'Installed profile DIP'

    return 0

def installProfileWorkflow(): # Profile Workflow

    # create profile workflow dictionaries

    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440010',
	  'name':'Workflow xx for Pre-Ingest',
          'profile_type': 'workflow',
	  'type':'Implementation',
	  'status':'Draft',
	  'label':'Workflow Create SIP for Pre-Ingest',
	  'specification':'Any specification wrapped',
	  'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile Workflow')
    print 'Installed profile workflow'

    return 0

def installProfilePreservationMetadata(): # Profile Preservation Metadata

    # create profile preservation metadata dictionaries

    dct = {
          'id':'550e8400-e29b-41d4a716-446655440011',
          'name':'Preservation profile xx',
          'profile_type': 'preservation_metadata',
          'type':'Implementation',
          'status':'Draft',
          'label':'Preservation profile for AIP xxyy',
          'specification':'Any specification wrapped',
          'specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    Profile.objects.create(**dct)

    #logger.info('Installed Profile PreservationMetadata')
    print 'Installed profile preservation metadata'

    return 0


if __name__ == '__main__':
    installProfiles()

