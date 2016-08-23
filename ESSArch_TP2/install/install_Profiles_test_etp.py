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
from profiles.models import SubmissionAgreement, ProfileTransferProject, ProfileContentType, ProfileDataSelection, ProfileClassification, ProfileImport, ProfileSubmitDescription, ProfileSIP, ProfileAIP, ProfileDIP, ProfileWorkflow

# settings
site_profile = "SE" # SE_NEW, SE, NO, EC
#zone = "zone1" # ETP=zone1, ETA=zone2

def installProfiles(): # Install all different profiles

    # install default configuration
    installSubmissionAgreement()     		# Submission Agreement
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

    return 0

def installSubmissionAgreement(): # Submission Agreement

    # First remove all existing data
    #SubmissionAgreement.objects.all().delete()

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
	  'profile_transfer_project':'550e8400-e29b-41d4a716-446655440001',
	  'profile_content_type':'550e8400-e29b-41d4a716-446655440002',
	  'profile_data_selection':'550e8400-e29b-41d4a716-446655440003',
	  'profile_classification':'550e8400-e29b-41d4a716-446655440004',
	  'profile_import':'550e8400-e29b-41d4a716-446655440005',
	  'profile_submit_description':'550e8400-e29b-41d4a716-446655440006',
	  'profile_sip':'550e8400-e29b-41d4a716-446655440007',
	  'profile_aip':'550e8400-e29b-41d4a716-446655440008',
	  'profile_dip':'550e8400-e29b-41d4a716-446655440009',
	  'profile_workflow':'550e8400-e29b-41d4a716-446655440010',
          }

    # create according to model with many fields
    SubmissionAgreement.objects.create(**dct)

    #logger.info('Installed Submission Agreement')
    print 'Installed submission agreement'

    return 0

def installProfileTransferProject(): # Profile Transfer Project

    # First remove all existing data
    #ProfileTransferProject.objects.all().delete()

    # create profile transfer project dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440001',
	  'profile_transfer_project_name':'SE ERMS Delivery',
	  'profile_transfer_project_type':'Implementation',
	  'profile_transfer_project_status':'Agreed',
	  'profile_transfer_project_label':'Example of SIP for delivery of SE ERMS',
	  'archive_policy':'Archive policy 1',
	  'container_format':'TAR',
	  'container_format_compression':'None',
	  'submission_reception_validation':'Yes',
	  'submission_reception_exception_handling':'None',
	  'submission_reception_receipt_confirmation':'None',
	  'submission_risk':'None',
	  'submission_mitigation':'None',
	  'information_package_file':'ip.xml',
	  'submission_information_package_file':'sip.xml',
	  'archival_information_package_file':'aip.xml',
	  'dissemination_information_package_file':'dip.xml',
	  'submit_description_file':'info.xml / ip_uuid',
	  'content_type_specification_file':'erms.xml / siard.xml / etc',
	  'archival_description_file':'ead.xml',
	  'authority_information_file':'eac_cpf.xml',
	  'preservation_description_file':'premis.xml',
	  'ip_event_description_file':'ipevents.xml',
	  'mimetypes_definition_file':'mime.types',
	  'preservation_organization_receiver_email':'receiver@archive.xxx',
	  'preservation_organization_receiver_url':'https://eta-demo.essarch.org,reta,reta',
          }

    # create according to model with many fields
    ProfileTransferProject.objects.create(**dct)

    #logger.info('Installed Profile Transfer Project')
    print 'Installed profile transfer project'

    return 0

def installProfileContentType(): # Profile Content Type

    # First remove all existing data
    #ProfileContentType.objects.all().delete()

    # create profile content type dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440002',
	  'profile_content_type_name':'SE ERMS',
	  'profile_content_type_type':'Implementation',
	  'profile_content_type_status':'Draft',
	  'profile_content_type_label':'Content based on SE ERMS specification',
	  'profile_content_type_specification':'Any specification wrapped',
          }

    # create according to model with many fields
    ProfileContentType.objects.create(**dct)

    #logger.info('Installed Profile Content Type')
    print 'Installed profile content type'

    return 0

def installProfileDataSelection(): # Profile Data Selection

    # First remove all existing data
    #ProfileDataSelection.objects.all().delete()

    # create profile data selection dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440003',
	  'profile_data_selection_name':'Classification of business system xx',
	  'profile_data_selection_type':'Implementation',
	  'profile_data_selection_status':'Draft',
	  'profile_data_selection_label':'Data selection of business system xx',
	  'profile_data_selection_specification':'Any specification wrapped',
          }

    # create according to model with many fields
    ProfileDataSelection.objects.create(**dct)

    #logger.info('Installed Profile Data Selection')
    print 'Installed profile data selection'

    return 0

def installProfileClassification(): # Profile Classification

    # First remove all existing data
    #ProfileClassification.objects.all().delete()

    # create profile classification dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440004',
	  'profile_classification_name':'Classification of archived objects',
	  'profile_classification_type':'Implementation',
	  'profile_classification_status':'Draft',
	  'profile_classification_label':'Classification of archived content',
	  'profile_classification_specification':'Any specification wrapped',
          }

    # create according to model with many fields
    ProfileClassification.objects.create(**dct)

    #logger.info('Installed Profile Classification')
    print 'Installed profile classification'

    return 0

def installProfileImport(): # Profile Import

    # First remove all existing data
    #ProfileImport.objects.all().delete()

    # create profile import dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440005',
	  'profile_import_name':'Transformation import profile for system xx',
	  'profile_import_type':'Implementation',
	  'profile_import_status':'Draft',
	  'profile_import_label':'Transformation from system x to specification y',
	  'profile_import_specification':'Any specification wrapped',
          }

    # create according to model with many fields
    ProfileImport.objects.create(**dct)

    #logger.info('Installed Profile Import')
    print 'Installed profile import'

    return 0

def installProfileSubmitDescription(): # Profile Submit Description

    # First remove all existing data
    #ProfileSubmitDescription.objects.all().delete()

    # create profile submit description dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440006',
	  'profile_sd_name':'Submit description of a single SIP',
	  'profile_sd_type':'Implementation',
	  'profile_sd_status':'Draft',
	  'profile_sd_label':'Desription of a one2one SIP2AIP',
	  'profile_sd_specification':'Any specification wrapped',
          }

    # create according to model with many fields
    ProfileSubmitDescription.objects.create(**dct)

    #logger.info('Installed Profile Submit Description')
    print 'Installed profile submit description'

    return 0

def installProfileSIP(): # Profile Submission Information Package

    # First remove all existing data
    #ProfileSIP.objects.all().delete()

    # create profile submission information package dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440007',
	  'profile_sip_name':'SIP based on SE FGS Package',
	  'profile_sip_type':'Implementation',
	  'profile_sip_status':'Draft',
	  'profile_sip_label':'SIP profile for SE submissions',
	  'sip_representation_info':'Documentation 1',
	  'sip_preservation_descriptive_info':'Documentation 2',
	  'sip_supplemental':'Documentation 3',
	  'sip_access_constraints':'Documentation 4',
	  'sip_datamodel_reference':'Documentation 5',
	  'sip_additional':'Documentation 6',
	  'sip_submission_method':'Electronically',
	  'sip_submission_schedule':'Once',
	  'sip_submission_data_inventory':'According to submit description',
	  'sip_structure':'SIP SE structure xx',
	  'sip_specification':'Any specification wrapped',
	  'sip_specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    ProfileSIP.objects.create(**dct)

    #logger.info('Installed Profile SIP')
    print 'Installed profile SIP'

    return 0

def installProfileAIP(): # Profile Archival Information Package

    # First remove all existing data
    #ProfileAIP.objects.all().delete()

    # create profile archival information package dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440008',
	  'profile_aip_name':'AIP based on SE FGS Package',
	  'profile_aip_type':'Implementation',
	  'profile_aip_status':'Draft',
	  'profile_aip_label':'AIP profile for SE Packages',
	  'aip_representation_info':'Documentation 1',
	  'aip_preservation_descriptive_info':'Documentation 2',
	  'aip_supplemental':'Documentation 3',
	  'aip_access_constraints':'Documentation 4',
	  'aip_datamodel_reference':'Documentation 5',
	  'aip_additional':'Documentation 6',
	  'aip_submission_method':'Electronically',
	  'aip_submission_schedule':'Once',
	  'aip_submission_data_inventory':'According to submit description',
	  'aip_structure':'AIP SE structure xx',
	  'aip_specification':'Any specification wrapped',
	  'aip_specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    ProfileAIP.objects.create(**dct)

    #logger.info('Installed Profile AIP')
    print 'Installed profile AIP'

    return 0

def installProfileDIP(): # Profile Dissemination Information Package

    # First remove all existing data
    #ProfileDIP.objects.all().delete()

    # create profile dissemination information package dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440009',
	  'profile_dip_name':'DIP based on SE FGS Package',
	  'profile_dip_type':'Implementation',
	  'profile_dip_status':'Draft',
	  'profile_dip_label':'DIP profile for SE Packages',
	  'dip_representation_info':'Documentation 1',
	  'dip_preservation_descriptive_info':'Documentation 2',
	  'dip_supplemental':'Documentation 3',
	  'dip_access_constraints':'Documentation 4',
	  'dip_datamodel_reference':'Documentation 5',
	  'dip_additional':'Documentation 6',
	  'dip_submission_method':'Electronically',
	  'dip_submission_schedule':'Once',
	  'dip_submission_data_inventory':'According to submit description',
	  'dip_structure':'DIP SE structure xx',
	  'dip_specification':'Any specification wrapped',
	  'dip_specification_data':'Any specification data wrapped',
          }

    # create according to model with many fields
    ProfileDIP.objects.create(**dct)

    #logger.info('Installed Profile DIP')
    print 'Installed profile DIP'

    return 0

def installProfileWorkflow(): # Profile Workflow

    # First remove all existing data
    #ProfileWorkflow.objects.all().delete()

    # create profile workflow dictionaries
    dct = {
	  'id':'550e8400-e29b-41d4a716-446655440010',
	  'profile_workflow_name':'Workflow xx for Pre-Ingest',
	  'profile_workflow_type':'Implementation',
	  'profile_workflow_status':'Draft',
	  'profile_workflow_label':'Workflow Create SIP for Pre-Ingest',
	  'profile_workflow_specification':'Any specification wrapped',
          }

    # create according to model with many fields
    ProfileWorkflow.objects.create(**dct)

    #logger.info('Installed Profile Workflow')
    print 'Installed profile workflow'

    return 0

if __name__ == '__main__':
    installProfiles()

