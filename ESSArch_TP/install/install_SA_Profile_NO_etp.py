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

# Create your views here.
from django.template import Context, loader
from django.template import RequestContext 
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.views import password_change as admin_password_change
import sys, logging, datetime, os

# own models etc
from profiles.models import AgentProfile, TransferProjectProfile, ImportProfile, DataSelectionProfile, ClassificationProfile
#import lib.utils as lu
#import lib.app_tools as lat

# settings
site_profile = "NO" # SE_NEW, SE, NO, EC
zone = "zone1" # ETP=zone1, ETA=zone2

def installProfiles(): # Install all different profiles

    # install default configuration
    installAgentProfile() 	     	# Agent Profile
    installTransferProjectProfile() 	# Transfer Project Profile
    installImportProfile() 		# Import Profile
    installDataSelectionProfile() 	# Data Selection Profile
    installClassificationProfile() 	# Classification Profile

    return 0

    
def installAgentProfile(): # Agent Profile
    
    # First remove all existing data 
    #AgentProfile.objects.all().delete()

    # create agent profile dictionaries 
    dct = {
    	  'agent_profile':'NAN',
    	  'agent_profile_id':'NAN 1',
          'agent_profile_type':'Main',
          'agent_profile_status':'NEW',
    	  'label':'Agent profile for National Archives of Norway',   
    	  'submission_agreement':'NAN 13-2011/5329; 2012-04-12',
          'archivist_organization':'Government X',
          'archivist_organization_id':'ORG:2010340910',
          'archivist_organization_software':'HR Employed',
          'archivist_organization_software_id':'5.0.34',
          'archivist_organization_software_type':'Noark 5',
          'archivist_organization_software_type_version':'1.2.3',
          'archivist_individual':'Elton John',
          'archivist_individual_telephone':'+46 (0)8-12 34 56',
          'archivist_individual_email':'Elton.John@company.se',
          'creator_organization':'Government X, Dep Y',
          'creator_organization_id':'ORG:2010340920',
          'creator_individual':'Mike Oldfield',
          'creator_individual_details':'+46 (0)8-12 34 56, Mike.Oldfield@company.se',
          'creator_individual_telephone':'+46 (0)8-12 34 56',
          'creator_individual_email':'Mike.Oldfield@company.se',
          'creator_software':'Packageprogram Packager',
          'creator_software_id':'1.0',
          'producer_organization':'Government X, Archival Dep',
          'producer_organization_id':'ORG:2010340930',
          'producer_individual':'Gene Simmons',
          'producer_individual_telephone':'+46 (0)8-12 34 56',
          'producer_individual_email':'Gene.Simmons@company.se',
          'producer_organization_software':'Government X system ',
          'producer_organization_software_identity':'Government X system version',
          'producer_organization_software_type':'Government X system type',
          'producer_organization_software_type_version':'Government X system type version',
          'submitter_organization':'Government X, Service Dep',
          'submitter_organization_id':'ORG:2010340940',
          'submitter_individual':'Lita Ford',
          'submitter_individual_telephone':'+46 (0)8-12 34 56',
          'submitter_individual_email':'Lita.Ford@company.se',
          'ipowner_organization':'Government X, Legal Dep',
          'ipowner_organization_id':'ORG:2010340950',
          'ipowner_individual':'Ozzy Osbourne',
          'ipowner_individual_telephone':'+46 (0)8-12 34 56',
          'ipowner_individual_email':'Ozzy.Osbourne@company.se',
          'editor_organization':'Consultancy Company',
          'editor_organization_id':'ORG:2020345960',
          'preservation_organization':'National Archives of X',
          'preservation_organization_id':'ORG:2010340970',
          'preservation_organization_software':'ESSArch',
          'preservation_organization_software_id':'3.0.0',
          }

    # create according to model with many fields
    AgentProfile.objects.create(**dct)

    #logger.info('Installed agent profile')
    print 'Installed agent profile'

    return 0


def installTransferProjectProfile(): # Transfer Project Profile

    # First remove all existing data
    #TransferProjectProfile.objects.all().delete()

    # create transfer project profile dictionaries
    dct = {
          'transfer_project_profile':'Transfer project type ERMS',
          'transfer_project_profile_id':'TPP 1, version 1.1.2',
          'transfer_project_profile_type':'SIP',
          'transfer_project_profile_status':'NEW',
          'label':'Example of SIP for delivery of ERMS',
          'system_type':'Noark 5 ver. xx',
          'submission_agreement':'NAN 13-2011/5329; 2012-04-12',
          'previous_submission_agreement':'FM 12-2387/12726, 2007-09-19',
          'data_submission_session':'Submission, 2012-04-15 15:00',
          'package_number':'SIP Number 2938',
          'referencecode':'SE/RA/123456/24/P',
          'previous_referencecode':'SE/FM/123/123.1/123.1.3',
          'appraisal':'Yes',
          'accessrestrict':'Secrecy and PUL',
          'archive_policy':'Archive Policy 1',
          'container_format':'TAR',
          'container_format_compression':'No',
          'informationclass':'1',
          }

    # create according to model with many fields
    TransferProjectProfile.objects.create(**dct)

    #logger.info('Installed transfer project profile')
    print 'Installed transfer project profile'

    return 0


def installImportProfile(): # Import Profile

    # First remove all existing data
    #ImportProfile.objects.all().delete()

    # create import profile dictionaries
    dct = {
          'import_profile':'Import from system XX',
          'import_profile_id':'1.2.3',
          'import_profile_type':'Business system xx',
          'import_profile_status':'NEW',
          'label':'Example of import profile',
          'submission_agreement':'xx 13-2011/5329; 2012-04-12',
          }

    # create according to model with many fields
    ImportProfile.objects.create(**dct)

    #logger.info('Installed import profile')
    print 'Installed import profile'

    return 0


def installDataSelectionProfile(): # Data Selection Profile

    # First remove all existing data
    #DataSelectionProfile.objects.all().delete()

    # create data selection profile dictionaries
    dct = {
          'data_selection_profile':'FGS ERMS,version 1',
          'data_selection_profile_id':'1.2.3',
          'data_selection_profile_type':'ERMS',
          'data_selection_profile_status':'NEW',
          'label':'Example of data selection profile',
          'submission_agreement':'xx 13-2011/5329; 2012-04-12',
          }

    # create according to model with many fields
    DataSelectionProfile.objects.create(**dct)

    #logger.info('Installed data selection profile')
    print 'Installed data selection profile'

    return 0


def installClassificationProfile(): # Classification Profile

    # First remove all existing data
    #ClassificationProfile.objects.all().delete()

    # create classification profile dictionaries
    dct = {
          'classification_profile':'KLASSA',
          'classification_profile_id':'1.1.0',
          'classification_profile_type':'AAS',
          'classification_profile_status':'NEW',
          'label':'Example of classification profile',
          'submission_agreement':'xx 13-2011/5329; 2012-04-12',
          }

    # create according to model with many fields
    ClassificationProfile.objects.create(**dct)

    #logger.info('Installed classification profile')
    print 'Installed classification profile'

    return 0


if __name__ == '__main__':
    installProfiles()

