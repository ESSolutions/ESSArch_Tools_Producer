# -*- coding: UTF-8 -*-
"""
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
"""

import sys

import django
django.setup()

from django.contrib.auth.models import User, Group, Permission
from configuration.models import Parameter, Path, Schema, EventType

# settings
site_profile = "SE" # SE_NEW, SE, NO, EC
#zone = "zone1" # ETP=zone1, ETA=zone2

def installDefaultConfiguration(): # Install default configuration

    # install default configuration
    createDefaultUsers()	# Default users and groups
    installDefaultParameters()	# Default Parameters
    installDefaultPaths()	# Default Paths
    installDefaultSchemas()	# Default XML Schemas
    installDefaultEventTypes()	# Default IP events

    return 0


def createDefaultUsers(): # default users, groups and permissions
    
    # remove existing default users and groups
    try:
        User.objects.get(username='user').delete()
    except User.DoesNotExist:
        pass

    try:
        User.objects.get(username='admin').delete()
    except User.DoesNotExist:
        pass

    try:
        User.objects.get(username='sysadmin').delete()
    except User.DoesNotExist:
        pass

    try:
        Group.objects.get(name='User').delete()
    except Group.DoesNotExist:
        pass

    try:
        Group.objects.get(name='Admin').delete()
    except Group.DoesNotExist:
        pass

    try:
        Group.objects.get(name='Sysadmin').delete()
    except Group.DoesNotExist:
        pass

    # permissions for default users
    can_add_ip_event = Permission.objects.get(name='Can add Event Type')
    can_change_ip_event = Permission.objects.get(name='Can change Event Type')
    can_delete_ip_event = Permission.objects.get(name='Can delete Event Type')
    #can_add_ip = Permission.objects.get(name='Can add information package')
    #can_change_ip = Permission.objects.get(name='Can change information package')
    #can_delete_ip = Permission.objects.get(name='Can delete information package')    

    # permissions for default admin user
    #can_do_admin_stuff = Permission.objects.get(name='Can do admin stuff')

    # permissions for default sysadmin user
    #can_do_sysadmin_stuff = Permission.objects.get(name='Can do sysadmin stuff')

    # create groups
    usergroup, created = Group.objects.get_or_create(name='User')
    usergroup.permissions.clear()
    usergroup.permissions.add(can_add_ip_event, can_change_ip_event, can_delete_ip_event)
    admingroup, created = Group.objects.get_or_create(name='Admin')
    admingroup.permissions.clear()
    #admingroup.permissions.add(can_do_admin_stuff)
    sysadmingroup, created = Group.objects.get_or_create(name='Sysadmin')
    sysadmingroup.permissions.clear()
    #sysadmingroup.permissions.add(can_do_sysadmin_stuff)

    # create an ordinary user
    try:
        myuser = User.objects.get(username='user')
    except User.DoesNotExist:
        myuser = User.objects.create_user('user', 'usr1@essolutions.se', 'user')
        myuser.groups.add(usergroup)
        myuser.save()

    # create admin user 
    try:
        myuser = User.objects.get(username='admin')
    except User.DoesNotExist:
        myuser = User.objects.create_user('admin', 'admin@essolutions.se', 'admin')
        myuser.groups.add(admingroup)
        myuser.is_staff = 1
        myuser.save()

    # create sysadmin user
    try:
        myuser = User.objects.get(username='sysadmin')
    except User.DoesNotExist:
        myuser = User.objects.create_user('sysadmin', 'sysadmin@essolutions.se', 'sysadmin')
        myuser.groups.add(sysadmingroup)
        myuser.is_staff = 1
        myuser.is_superuser = 1
        myuser.save()
    print 'added users and groups'
    return 0
    
def installDefaultParameters(): # default config parameters

    # First remove all data
    Parameter.objects.all().delete()
    
    # Set default parameters
    dct = {
          'site_profile':site_profile,
          'smtp_server':'localhost',
          #'zone': zone ,
          #'package_descriptionfile':'info.xml',
          #'content_descriptionfile':'info.xml',
          #'preservation_descriptionfile':'premis.xml',
          #'ip_eventfile':'ipevents.xml',
          #'mimetypes_definition':'mime.types',
          #'preservation_organization_receiver':'False, example: http://xxx.xxx.xxx.xxx:5002,user,pass',
          #'preservation_email_receiver':'receiver@archive.xxx',
          }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = Parameter( entity=key, value=dct[key] )
            le.save()
        except:
            pass

    return 0


def installDefaultPaths(): # default paths

    # First remove all existing data 
    Path.objects.all().delete()
   
    # create dictionaries 
    dct = {
          'path_mimetypes_definitionfile':'/ESSArch/config/mime.types',
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

    
def installDefaultSchemas(): # default schema profiles for Sweden and Norway
    
    # First remove all existing data 
    Schema.objects.all().delete()

    # create schema dictionaries 
    dct = {
          'addml_namespace':'http://xml.ra.se/addml',
          'addml_schemalocation':'http://xml.ra.se/addml/ra_addml.xsd',
          'erms_schemalocation': 'http://xml.ra.se/e-arkiv/ERMS/version10/Arendehantering.xsd', # internal schema
          'mets_namespace': 'http://www.loc.gov/METS/',
          #'mets_profile': 'http://xml.ra.se/METS/RA_METS_eARD.xml',
          #'mets_profile': 'http://xml.ra.se/e-arkiv/METS/version20/eARD_Paket_FGS.xml',
          'mets_profile': 'http://xml.ra.se/e-arkiv/METS/version10/CommonSpecificationSwedenPackageProfile.xml',
          'mets_schemalocation': 'http://xml.ra.se/e-arkiv/METS/version10/CSPackageMETS.xsd', # public schema
          #'mets_schemalocation': 'http://xml.ra.se/e-arkiv/METS/version20/eARD_Paket_FGS_mets.xsd', # public schema
          #'mets_schemalocation': 'http://xml.ra.se/METS/RA_METS_eARD.xsd', # internal schema
          #'mets_schemalocation': 'http://xml.ra.se/e-arkiv/METS/eARD_Paket_FGS_mets.xsd', # public schema
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

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = Schema( entity=key, value=dct[key] )
            le.save()
        except:
            pass
    
    return 0


def installDefaultEventTypes(): # default IP events

    # First remove all existing data
    EventType.objects.all().delete()

    # create IP events dictionaries
    dct = {
          'Prepare IP':'10100',
          'Create SIP':'10200',
          'Submit SIP':'10300',
          }

    # create according to model with two fields
    for key in dct :
        print >> sys.stderr, "**", key
        try:
            le = EventType( eventType=dct[key], eventDetail=key )
            le.save()
        except:
            pass

    return 0


if __name__ == '__main__':
    installDefaultConfiguration()

