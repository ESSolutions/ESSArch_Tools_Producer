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

# Create your views here.
from django.template import Context, loader
from django.template import RequestContext 
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.views import password_change as admin_password_change
import sys, logging, datetime, os

# own models etc
from configuration.models import Parameter, LogEvent, SchemaProfile, IPParameter, Path
#import lib.utils as lu
#import lib.app_tools as lat

import django
django.setup()

# settings
site_profile = "NO" # SE_NEW, SE, NO, EC
zone = "zone1" # ETP=zone1, ETA=zone2

def installdefaultparameters(): # default config parameters

    # First remove all data 
    Parameter.objects.all().delete()

    # set default parameters according to site_profile SE
    if site_profile == "SE" :
       dct = {
             'site_profile':site_profile,
             'zone': zone ,
             'package_descriptionfile':'info.xml',
             'content_descriptionfile':'sip.xml',
             'preservation_descriptionfile':'premis.xml',
             'ip_logfile':'log.xml',
             'mimetypes_definition':'mime.types',
             'preservation_organization_url':'www.essolutions.se',
             'preservation_email_receiver':'receiver@archive.xxx',
             }

    # set default parameters according to site_profile NO
    if site_profile == "NO" :
        dct = {
              'site_profile':site_profile,
              'zone': zone ,
              'package_descriptionfile':'info.xml',
              'content_descriptionfile':'mets.xml',
              'preservation_descriptionfile':'premis.xml',
              'ip_logfile':'log.xml',
              'mimetypes_definition':'mime.types',
              'preservation_organization_url':'www.essolutions.se',
              'preservation_email_receiver':'receiver@archive.xxx',
              }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = Parameter( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    # install default configuration
    createdefaultusers()             # default users, groups and permissions
    installdefaultpaths()            # default paths
    installdefaultschemaprofiles()   # default schema profiles 
    installogdefaults()              # default logevents
    installIPParameter()             # default metadata for IP
    
    return 0


def createdefaultusers(): # default users, groups and permissions
    
    # remove existing default users
    for i in xrange(1,4):
        try:
            User.objects.get(username='usr'+str(i)).delete()
        except User.DoesNotExist:
            pass
    
    # remove existing default groups
    for i in xrange(1,4):
        try:
            Group.objects.get(name='Zone'+str(i)).delete()
        except Group.DoesNotExist:
            pass
    
    # permissions for default users
    can_add_log_entry = Permission.objects.get(name='Can add log entry')
    can_change_log_entry = Permission.objects.get(name='Can change log entry')
    can_delete_log_entry = Permission.objects.get(name='Can delete log entry')
    can_view_log_menu = Permission.objects.get(name='Can_view_log_menu')
    can_view_ip_menu = Permission.objects.get(name='Can_view_ip_menu')
    can_add_ip = Permission.objects.get(name='Can add information package')
    can_change_ip = Permission.objects.get(name='Can change information package')
    can_delete_ip = Permission.objects.get(name='Can delete information package')    

    # create admin superuser 
    try:
        myuser = User.objects.get(username='admin')
    except User.DoesNotExist:
        myuser = User.objects.create_user('admin', 'admin@essolutions.se', 'admin')
        myuser.is_staff = 1
        myuser.is_superuser = 1
        myuser.save()

    # create users and groups according
    try:
        myuser = User.objects.get(username='usr1')
    except User.DoesNotExist:
        myuser = User.objects.create_user('usr1', 'usr1@essolutions.se', 'usr1')
    mygroup, created = Group.objects.get_or_create(name='Zone1')
    myuser.groups.add(mygroup)
    mygroup.permissions.clear()
    mygroup.permissions.add(can_add_log_entry, can_change_log_entry, can_delete_log_entry, can_view_ip_menu, can_add_ip, can_change_ip, can_delete_ip)
    
    return 0
    

def installdefaultpaths(): # default paths

    # First remove all existing data 
    Path.objects.all().delete()

    # create dictionaries 
    dct = {
          #'path_mimetypesdefinition':'/ESSArch/Tools/env',
          'path_definitions':'/ESSArch/etp/env',
          'path_preingest_prepare':'/ESSArch/data/etp/prepare',
          'path_preingest_reception':'/ESSArch/data/etp/reception',
          'path_ingest_reception':'/ESSArch/data/eta/reception/eft',
          }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = Path( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    return 0

    
def installogdefaults(): # default logevents
    
    # First remove all existing data 
    LogEvent.objects.all().delete()

    # create logevents dictionaries 
    dct = {
          #'Log circular created':'10000',
          'Delivery is being prepared':'10100',
          'Delivery is created':'10200',
          'Ready for delivery':'10300',
          }
        
    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = LogEvent( eventType=dct[key], eventDetail=key )
            le.save()
        except:
            pass

    return 0


def installdefaultschemaprofiles(): # default schema profiles for Sweden and Norway
    
    # First remove all existing data 
    SchemaProfile.objects.all().delete()

    # find out which site_profile
    site_profile = Parameter.objects.get(entity="site_profile").value

    # create schema dictionaries per country SE/NO 
    if site_profile == "SE" :
        dct = {
              'addml_namespace':'http://xml.ra.se/addml',
              'addml_schemalocation':'http://xml.ra.se/addml/ra_addml.xsd',
              'erms_schemalocation': 'http://xml.ra.se/e-arkiv/ERMS/version10/Arendehantering.xsd', # internal schema
              'mets_namespace': 'http://www.loc.gov/METS/',
              #'mets_profile': 'http://xml.ra.se/METS/RA_METS_eARD.xml',
              'mets_profile': 'http://xml.ra.se/e-arkiv/METS/version20/eARD_Paket_FGS.xml',
              'mets_schemalocation': 'http://xml.ra.se/e-arkiv/METS/version20/eARD_Paket_FGS_mets.xsd', # public schema
              #'mets_schemalocation': 'http://xml.ra.se/METS/RA_METS_eARD.xsd', # internal schema
              #'mets_schemalocation': 'http://xml.ra.se/e-arkiv/METS/eARD_Paket_FGS_mets.xsd', # public schema
              #'mets_schemalocation': '/ESSArch/Tools/env/eARD_Paket_FGS_mets.xsd',
              'mets_schemalocation_local': 'http://xml.ra.se/e-arkiv/METS/version20/eARD_Paket_FGS_mets.xsd', # public schema
              'mix_namespace':'http://xml.ra.se/MIX',
              'mix_schemalocation':'http://xml.ra.se/MIX/RA_MIX.xsd',
              'mods_namespace':'http://www.loc.gov/mods/v3',
              'personnel_schemalocation': 'http://xml.ra.se/e-arkiv/Personnel/version10/Personal.xsd', # internal schema
              'premis_namespace':'http://xml.ra.se/PREMIS',
              #'premis_schemalocation':'http://xml.ra.se/PREMIS/RA_PREMIS.xsd',
              'premis_schemalocation':'http://xml.ra.se/PREMIS/ESS/RA_PREMIS_PreVersion.xsd',
              'premis_version':'2.0',
              'xhtml_namespace':'http://www.w3.org/1999/xhtml',
              'xhtml_schemalocation':'http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd',
              'xlink_namespace':'http://www.w3.org/1999/xlink',
              'xsd_namespace':'http://www.w3.org/2001/XMLSchema',
              'xsi_namespace':'http://www.w3.org/2001/XMLSchema-instance',
              }

    if site_profile == "NO" :
        dct = {
              'addml_namespace': 'http://www.arkivverket.no/addml',
              'addml_schemalocation': 'http://schema.arkivverket.no/ADDML/v8.2/addml.xsd',
              'mets_namespace': 'http://www.loc.gov/METS/',
              'mets_profile': 'http://xml.ra.se/METS/RA_METS_eARD.xml',
              'mets_schemalocation': 'http://schema.arkivverket.no/METS/info.xsd', # public schema
              'mets_schemalocation_local': 'http://schema.arkivverket.no/METS/mets.xsd', # public schema
              'mix_namespace': 'http://xml.ra.se/MIX',
              'mix_schemalocation': 'http://xml.ra.se/MIX/RA_MIX.xsd',
              'mods_namespace': 'http://www.loc.gov/mods/v3',
              'premis_namespace': 'http://arkivverket.no/standarder/PREMIS',
              'premis_schemalocation': 'http://schema.arkivverket.no/PREMIS/v2.0/DIAS_PREMIS.xsd',
              'premis_version': '2.0',
              'xhtml_namespace': 'http://www.w3.org/1999/xhtml',
              'xhtml_schemalocation': 'http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd',
              'xlink_namespace': 'http://www.w3.org/1999/xlink',
              'xsd_namespace': 'http://www.w3.org/2001/XMLSchema',
              'xsi_namespace': 'http://www.w3.org/2001/XMLSchema-instance',
              }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = SchemaProfile( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    return 0


def installIPParameter():  # default metadata for IP

    # First remove all data 
    IPParameter.objects.all().delete()
    
    # find out which site_profile
    site_profile = Parameter.objects.get(entity="site_profile").value

    # create dictionary for IP elements
    #if site_profile == "SE" :
    #if site_profile == "NO" :
    dct = {
          'objid':'UUID:550e8400-e29b-41d4-a716-446655440004',
          'label':'Example of SIP for delivery of personnel information',
          'type':'SIP',
          'createdate':'2012-04-26T12:45:00+01:00',
          'recordstatus':'NEW',
          'deliverytype':'ERMS',
          'deliveryspecification':'FGS Personnel, version 1',
          'submissionagreement':'RA 13-2011/5329; 2012-04-12',
          'systemtype':'Noark 5 ver. xx',
          'previoussubmissionagreement':'FM 12-2387/12726, 2007-09-19',
          'datasubmissionsession':'Submission, 2012-04-15 15:00',
          'packagenumber':'SIP Number 2938',
          'referencecode':'SE/RA/123456/24/P',
          'previousreferencecode':'SE/FM/123/123.1/123.1.3',
          'appraisal':'Yes',
          'accessrestrict':'Secrecy and PUL',
          'startdate':'2012-01-01', 
          'enddate':'2012-12-30',
          'informationclass':'1',
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
          'file_id':'ID550e8400-e29b-41d4-a716-4466554400bg', 
          'file_name':'file:personalexport.xml',
          'file_createdate':'2012-04-20T13:30:00,+01:00',
          'file_mime_type':'text/xml',
          'file_format':'PDF/A',
          'file_size':'8765324',
          'file_type':'Delivery file',
          'file_function':'new value',
          'file_checksum':'574b69cf71ceb5534c8a2547f5547d',
          'file_checksum_type':'SHA-256',
          'file_transform_type':'DES',
          'file_transform_key':'574b69cf71ceb5534c8a2547f5547d',
          'comments':'Any comments',
          'aic_id':'e4d025bc-56b0-11e2-893f-002215836551',
          'projectname':'Scanning',
          'policyid':'1',
          'receipt_email':'Mike.Oldfield@company.se',
          }
    
    #print dict1.keys()
    #print dict1.values()
    #print dict1.items()
    #print tt3.items()
    
    #new_dict = {}
    #new_lst = []
    
    #new_dict.update(dict2)
    #new_dict.update(dict3)
    #print new_dict.items() 

    # create according to model with many fields
    IPParameter.objects.create(**dct)
    #IPMetadata.objects.create(**dct1)  # create from dictionary
    #IPMetadata.objects.filter(id=1).update(**dct1)  # update from dictionary

    return 0

if __name__ == '__main__':
    installdefaultparameters()

