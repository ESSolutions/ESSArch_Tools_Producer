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

from django.template import Context, loader 
from django.http import Http404
from lxml import etree
from urllib2 import Request, urlopen, URLError, HTTPError
import os, sys, pytz, datetime, uuid, mimetypes, stat, hashlib, tarfile, time, shutil, urllib, platform

# import the logging library and get an instance of a logger
import logging
logger = logging.getLogger('code.exceptions')

# own models etc
from ip.models import InformationPackage
from configuration.models import LogEvent, Parameter, SchemaProfile, Path, IPParameter
import mets_eARD as m 
import utils, ESSMD, ESSPGM


###############################################
"Agent list for site profile SE"
"""
ET090 - BS130301 - Ready for test
"""
def create_AgentList_SE(ip, contextdata):
    version = 'ET090'
    logger.debug('%s Entered create_AgentList_SE' % version) # debug info
            
    # agent lists
    agent_list = []
    # list 1
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    #name = contextdata['archivist_organization']
    name = ip.archivist_organization
    note = contextdata['archivist_organization_id']
    if len(name) and len(note):
        agent_list.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 2
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'OTHER'
    OTHERTYPE = 'SOFTWARE'
    name = contextdata['archivist_organization_software']
    note = None
    if len(name):
        if note == None:
            agent_list.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 3
    ROLE = 'CREATOR'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['creator_organization']
    note = None
    if len(name):
        if note == None:
            agent_list.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])

    return agent_list


###############################################
"altRecordID list for site profile NO"
"""
ET090 - BS130301 - Ready for test
"""
def create_altRecordIDList_SE(ip, contextdata):
    version = 'ET090'
    logger.debug('%s Entered create_altRecordIDList_SE' % version) # debug info
                
    # altRecordID lists
    altRecordID_list = []
    # list 1
    TYPE = 'DELIVERYTYPE'
    value = contextdata['deliverytype']
    if len(value):
        altRecordID_list.append([TYPE,value])
    # list 2
    TYPE = 'DELIVERYSPECIFICATION'
    value = contextdata['deliveryspecification']
    if len(value):
        altRecordID_list.append([TYPE,value])
    # list 3
    TYPE = 'SUBMISSIONAGREEMENT'
    value = contextdata['submissionagreement']
    if len(value):
        altRecordID_list.append([TYPE,value])
    # list 4
    #TYPE = 'PREVIOUSSUBMISSIONAGREEMENT'
    #value = contextdata['previoussubmissionagreement']
    #if len(value):
    #    altRecordID_list.append([TYPE,value])
    # list 5
    #TYPE = 'STARTDATE'
    #value = contextdata['startdate']
    ##value = ip.startdate
    #if len(value):
    #    altRecordID_list.append([TYPE,value])
    # list 6
    #TYPE = 'ENDDATE'
    #value = contextdata['enddate']
    ##value = ip.enddate
    #if len(value):
    #    altRecordID_list.append([TYPE,value])

    return altRecordID_list


###############################################
"Agent lists for site profile NO"
"""
ET090 - BS130301 - Ready for test
"""
def create_AgentList_NO(ip, contextdata):
    version = 'ET090'
    logger.debug('%s Entered create_AgentList_NO' % version) # debug info
            
    # agent lists
    agent_list_info = [] # list for info.xml
    agent_list_mets = [] # list for mets.xml
    # list 1
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    #name = contextdata['archivist_organization']
    name = ip.archivist_organization
    #note = contextdata['archivist_organization_id']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 2
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'OTHER'
    OTHERTYPE = 'SOFTWARE'
    name = contextdata['archivist_organization_software']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 3
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'OTHER'
    OTHERTYPE = 'SOFTWARE'
    name = contextdata['archivist_organization_software_id']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 4
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'OTHER'
    OTHERTYPE = 'SOFTWARE'
    name = contextdata['archivist_organization_software_type']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 5
    ROLE = 'CREATOR'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['creator_organization']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 6
    ROLE = 'OTHER'
    OTHERROLE = 'PRODUCER'
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['producer_organization']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 7
    ROLE = 'OTHER'
    OTHERROLE = 'PRODUCER'
    TYPE = 'INDIVIDUAL'
    OTHERTYPE = None
    name = contextdata['producer_individual']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 8
    ROLE = 'OTHER'
    OTHERROLE = 'PRODUCER'
    TYPE = 'OTHER'
    OTHERTYPE = 'SOFTWARE'
    name = contextdata['producer_organization_software_type']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 9
    ROLE = 'OTHER'
    OTHERROLE = 'SUBMITTER'
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['submitter_organization']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 10
    ROLE = 'OTHER'
    OTHERROLE = 'SUBMITTER'
    TYPE = 'INDIVIDUAL'
    OTHERTYPE = None
    name = contextdata['submitter_individual']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 11
    ROLE = 'IPOWNER'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['ipowner_organization']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 12
    ROLE = 'PRESERVATION'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['preservation_organization']
    note = None
    #note = contextdata['preservation_organization_id']
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            
    return agent_list_info, agent_list_mets

###############################################
"Agent lists for site profile NO"
"""
ET090 - BS130301 - Ready for test
"""
def create_AgentList_EC(ip, contextdata):
    version = 'ET090'
    logger.debug('%s Entered create_AgentList_NO' % version) # debug info
            
    # agent lists
    agent_list_info = [] # list for info.xml
    agent_list_mets = [] # list for mets.xml
    # list 1
    ROLE = 'ARCHIVIST'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    #name = contextdata['archivist_organization']
    name = ip.archivist_organization
    #note = contextdata['archivist_organization_id']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 9
    ROLE = 'OTHER'
    OTHERROLE = 'SUBMITTER'
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['submitter_organization']
    note = None
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
    # list 12
    ROLE = 'PRESERVATION'
    OTHERROLE = None
    TYPE = 'ORGANIZATION'
    OTHERTYPE = None
    name = contextdata['preservation_organization']
    note = None
    #note = contextdata['preservation_organization_id']
    if len(name):
        if note == None:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[]])
        else:
            agent_list_info.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            agent_list_mets.append([ROLE,OTHERROLE,TYPE,OTHERTYPE,name,[note]])
            
    return agent_list_info, agent_list_mets

###############################################
"altRecordID lists for site profile NO"
"""
ET090 - BS130301 - Ready for test
"""
def create_altRecordIDList_NO(ip, contextdata):                 
    version = 'ET090'
    logger.debug('%s Entered create_altRecordIDList_NO' % version) # debug info
    
    # altRecordID lists
    altRecordID_list_info = [] # list for info.xml
    altRecordID_list_mets = [] # list for mets.xml
    # list 1
#        TYPE = 'DELIVERYTYPE'
#        value = contextdata['deliverytype']
#        if len(value):
#            altRecordID_list_info.append([TYPE,value])
#            altRecordID_list_mets.append([TYPE,value])
    # list 2
#        TYPE = 'DELIVERYSPECIFICATION'
#        value = contextdata['deliveryspecification']
#        if len(value):
#            altRecordID_list_info.append([TYPE,value])
#            altRecordID_list_mets.append([TYPE,value])
    # list 3
    TYPE = 'SUBMISSIONAGREEMENT'
    value = contextdata['submissionagreement']
    if len(value):
        altRecordID_list_info.append([TYPE,value])
        altRecordID_list_mets.append([TYPE,value])
    # list 4
#        TYPE = 'SYSTEMTYPE'
#        value = contextdata['systemtype']
#        if len(value):
#            altRecordID_list_info.append([TYPE,value])
#            altRecordID_list_mets.append([TYPE,value])
    # list 5
    TYPE = 'STARTDATE'
    value = contextdata['startdate']
    #value = ip.startdate
    if len(value):
        altRecordID_list_info.append([TYPE,value])
        altRecordID_list_mets.append([TYPE,value])
    # list 6
    TYPE = 'ENDDATE'
    value = contextdata['enddate']
    #value = ip.enddate
    if len(value):
        altRecordID_list_info.append([TYPE,value])
        altRecordID_list_mets.append([TYPE,value])
            
    return altRecordID_list_info, altRecordID_list_mets

###############################################
"altRecordID lists for site profile NO"
"""
ET090 - BS130301 - Ready for test
"""
def create_altRecordIDList_EC(ip, contextdata):                 
    version = 'ET090'
    logger.debug('%s Entered create_altRecordIDList_NO' % version) # debug info
    
    # altRecordID lists
    altRecordID_list_info = [] # list for info.xml
    altRecordID_list_mets = [] # list for mets.xml
    # list 1
#        TYPE = 'DELIVERYTYPE'
#        value = contextdata['deliverytype']
#        if len(value):
#            altRecordID_list_info.append([TYPE,value])
#            altRecordID_list_mets.append([TYPE,value])
    # list 2
#        TYPE = 'DELIVERYSPECIFICATION'
#        value = contextdata['deliveryspecification']
#        if len(value):
#            altRecordID_list_info.append([TYPE,value])
#            altRecordID_list_mets.append([TYPE,value])
    # list 3
    TYPE = 'SUBMISSIONAGREEMENT'
    value = contextdata['submissionagreement']
    if len(value):
        altRecordID_list_info.append([TYPE,value])
        altRecordID_list_mets.append([TYPE,value])
    # list 4
#        TYPE = 'SYSTEMTYPE'
#        value = contextdata['systemtype']
#        if len(value):
#            altRecordID_list_info.append([TYPE,value])
#            altRecordID_list_mets.append([TYPE,value])
    # list 5
    TYPE = 'STARTDATE'
    #value = contextdata['startdate']
    value = '2016-04-12'
    #value = ip.startdate
    if len(value):
        altRecordID_list_info.append([TYPE,value])
        altRecordID_list_mets.append([TYPE,value])
    # list 6
    TYPE = 'ENDDATE'
    #value = contextdata['enddate']
    value = '2016-04-12'
    #value = ip.enddate
    if len(value):
        altRecordID_list_info.append([TYPE,value])
        altRecordID_list_mets.append([TYPE,value])
   
    return altRecordID_list_info, altRecordID_list_mets

###############################################
"Prepare information package (IP)"
"""
ET090 - BS130301 - Ready for test
"""
def prepareIP( agent, contextdata ):
    version = 'ET090'
    logger.debug('%s Entered prepareIP' % version) # debug info
    logger.info('Preparing IP') # info for logfile
    
    # get current site_profile and zone
    site_profile, zone = getSiteZone()

    # get template files
    parameters = Parameter.objects.all()
    templatefile_log = parameters.get(entity="ip_logfile").value
    templatefile_cspec = parameters.get(entity="content_descriptionfile").value
    templatefile_pspec = parameters.get(entity="package_descriptionfile").value
    
    # need to find out path to log files
    logfilepath = getLogFilePath()

    ##### zone1 #####
    
    # create related metadata for zone1
    if zone == 'zone1' :

        # get data from form
        try:
            destinationroot = contextdata["destinationroot"]
        except:
            destinationroot = getLogFilePath()

        # Create a new information package folder
        i = 1
        while os.path.exists( os.path.join( destinationroot, "ip%d"%i ) ):
            i+=1
        root = os.path.join( destinationroot, "ip%d"%i )
        os.makedirs( root )

        # create IP_UUID sub-folder for the IP
        ip_uuid =  str( uuid.uuid1())
        iproot = createIPdirectory(root, ip_uuid)
        #iproot = createIPdirectory(root, ip_uuid, site_profile)

        # package info type
        contextdata["iptype"] = 'SIP'

        # create aic_uuid for zone1
        aic_uuid = ""
        
        # initial event for preparation of IP in zone1
        eventType = 10000   # type of event
        eventDetail = 'Log circular created'  # event detail
        state = "Prepared"  # state
        progress = 100  # progress  

        ##### zone1 end #####
    
    ##### zone2 start #####

    # create related metadata for zone2
    if zone == 'zone2':

        # path to reception
        reception = Path.objects.get(entity="path_reception").value

        # keep track of error descriptions etc
        status_list = []
        error_list = []
        status_code = 0

        # parse context from specification file
        #filename = contextdata["sourceroot"]+'/'+templatefile_pspec
        filename = contextdata["filename"]
        if os.path.exists(filename):
            context = ParseSpecFile(filename)
        else:
            status_code = 201
            error_list.append('Package description file %s does not exist' % filename)
            return 1, status_code, error_list
        
        # if asked for validate inner mets-file
        if contextdata["package_description"] == 'Yes':
            XMLSchema = SchemaProfile.objects.get(entity='mets_schemalocation').value
            errno, why = validate(FILENAME=filename, XMLSchema=XMLSchema)
            if errno:
                status_code = 202
                error_list.append('Could not validate package description file %s Reason: %s' % (filename, why))
            else:
                status_list.append('Successfully validated package description file %s' % filename)
                
        # if asked for validate logical and physical representation of objects 
        if contextdata["package_content"] == 'Yes':
            # define checksum algoritm, timezone etc
            if site_profile == 'SE' :
                checksumtype = 1 # MD5
                checksumalgoritm = 'MD5'
                TimeZone = 'Europe/Stockholm'
                
            if  site_profile == 'NO' : 
                checksumtype = 2 # SHA256
                checksumalgoritm = 'SHA-256'
                TimeZone = 'Europe/Stockholm'
                
            ObjectIdentifierValue = context['ip_uuid']  
            #ObjectPath = contextdata["sourceroot"]
            ObjectPath = contextdata["iplocation"]
            checksumtype_default = checksumalgoritm
            METS_ObjectPath = filename
            errno, result, reslist = DiffCheck_IP(ObjectIdentifierValue, ObjectPath, METS_ObjectPath, TimeZone, checksumtype_default)
            result_sum = len(reslist[0]) + len(reslist[1]) + len(reslist[2]) + len(reslist[3]) + len(reslist[4]) + len(reslist[5])
            if result_sum != len(reslist[0]):
                status_code = 203
                error_list.append('Physical files mismatch the logical representation of content description file %s Reason: %s' % (METS_ObjectPath, result[0]))
            else:
                status_list.append('Physical files match the logical representation of content description file %s' % METS_ObjectPath)
 
        # TODO dev validation
        # if asked for validate delivery type specification file
        #if contextdata["deliverytype_description"] == 'Yes':
        #    # parse deliverytype from spec file
        #    if context["deliverytype"] == "ERMS":
        #        XMLSchema = SchemaProfile.objects.get(entity='erms_schemalocation').value
        #    if context["deliverytype"] == "Personnel":
        #        XMLSchema = SchemaProfile.objects.get(entity='personnel_schemalocation').value
        #    
        #     validate spec file
        #    errno, why = validate(FILENAME=filename, XMLSchema=XMLSchema)
        #    if errno:
        #        status_code = 204
        #        error_list.append('Could not validate package description file %s Reason: %s' % (filename, why))
        #    else:
        #        status_list.append('Successfully validated package description file %s' % filename)

        # if we had any errors log them
        if status_code == 0:
            for stat in status_list:
                logger.info(stat)
        else: 
            for err in error_list:
                logger.error(err)
            return 1, status_code, error_list
       
        # need to search through all log files to find any duplicates
        loglist = getLogFiles(logfilepath, templatefile_log)
        for log in loglist:
            if log["uuid"] == context["ip_uuid"] :
                raise Http404

        # package info
        #contextdata["creator"] = context["ip_creator"]
        contextdata["archivist_organization"] = context["ip_archivist_organization"]
        contextdata["label"] = context["ip_label"]
        #contextdata["startdate"] = context["ip_startdate"]
        #contextdata["enddate"] = context["ip_enddate"]
        contextdata["iptype"] = context["ip_type"]
        contextdata["createdate"] = context["ip_createdate"]

        # create aic_uuid
        try :
            aic_uuid = context["aic_uuid"]
        except:
            aic_uuid = str(uuid.uuid1())
                
        # create ip_uuid
        if context["ip_uuid"][:5] == 'UUID:' or context["ip_uuid"][:5] == 'RAID:' : 
            ip_uuid = context["ip_uuid"][5:]
        else :
            ip_uuid = context["ip_uuid"]

        # create AIC_UUID directory
        root = createAICdirectory( logfilepath, aic_uuid )

        # create IP_UUID directory
        iproot = createIPdirectory( root, ip_uuid )
        #iproot = createIPdirectory( root, ip_uuid, site_profile )
        
        # copy specfile from source to destination
        src_specfile = filename
        dst_specfile = root+'/'+templatefile_pspec
        #shutil.copy(src_specfile, dst_specfile)
        shutil.move(src_specfile, dst_specfile)

        # copy IP from source to destination
        if site_profile == 'SE':
            #src_ipfile = contextdata["sourceroot"]+'/'+ip_uuid+'.tar'
            src_ipfile = contextdata["iplocation"]+'/'+ip_uuid+'.tar'
            dst_ipfile = root+'/'+ip_uuid +'/content/'+ip_uuid+'.tar'
            dst1_ipfile = reception+'/'+ip_uuid+'.tar'
            shutil.copy(src_ipfile, dst_ipfile)
            shutil.copy(src_ipfile, dst1_ipfile)
                
        # Initial event for preparation of IP in zone2
        eventType = 20000   # type of event
        eventDetail = 'Created log circular'  # event detail
        state = "Received"  # state
        progress = 100  # progress  

        ##### zone2 end #####
                    
    # creation timestamp regardless zone
    create_time = utils.creation_time('Europe/Stockholm')
            
    # common package info regardless zone
    contextdata["site_profile"] = site_profile
    contextdata["aic_uuid"] = aic_uuid
    contextdata["ip_uuid"] = ip_uuid
    contextdata["createdate"] = create_time
    contextdata["creation_time"] = create_time
    
    # schema profile regardless zone
    contextdata["premis_namespace"] = SchemaProfile.objects.get(entity='premis_namespace').value 
    contextdata["xsi_namespace"] = SchemaProfile.objects.get(entity='xsi_namespace').value
    contextdata["xlink_namespace"] = SchemaProfile.objects.get(entity='xlink_namespace').value
    contextdata["premis_schemalocation"] = SchemaProfile.objects.get(entity='premis_schemalocation').value
    contextdata["premis_version"] = SchemaProfile.objects.get(entity='premis_version').value

    # event regardless zone
    contextdata["eventIdentifierValue"] = str(uuid.uuid1())  # create unique event_uuid
#    contextdata["eventType"] = LogEvent.objects.get(eventType=eventType).eventType  # event code 
#    contextdata["eventDetail"] = LogEvent.objects.get(eventType=eventType).eventDetail  # event detail
    contextdata["eventType"] = eventType  # event code 
    contextdata["eventDetail"] = eventDetail  # event detail
    contextdata["eventOutcome"] = 0  # status = Ok 
    contextdata["eventOutcomeDetailNote"] = "Success to create logfile"  # comments
    contextdata["linkingAgentIdentifierValue"] = agent   # agent e.q user str(request.user) 
    contextdata["linkingObjectIdentifierValue"] = ip_uuid  # ipuuid
                
    # render template logfile
    t = loader.get_template( "xml/"+templatefile_log )
  
    # create log.xml and place it in IP folder
    logfilename = os.path.join( iproot, templatefile_log )
    logXML = open( logfilename, "w" )

    # write context to logfile
    c = Context(contextdata)
    logXML.write( t.render( c ).encode( "utf-8" ) )
    logXML.close()
 
    # everything is created in the filesystem, so now we create
    # a database entry for this IP
    ip = InformationPackage( archivist_organization = contextdata["archivist_organization"],
                             label = contextdata["label"],
                             #startdate = contextdata["startdate"],
                             #enddate = contextdata["enddate"],
                             createdate = contextdata["createdate"],
                             iptype = contextdata["iptype"],
                             uuid = ip_uuid,
                             directory = root,
                             site_profile = site_profile,
                             state = state,
                             zone = zone,
                             progress = progress )
    ip.save()
        
    # return status
    return ip, 0, "Ok"



###############################################
"Create information package (IP)"
"""
ET090 - BS130301 - Ready for test
ET091 - Bs130324 - Added debug and version logging
"""
def createIP( ip, contextdata ):
    version = 'ET091'
    logger.debug('%s Entered createIP' % version) # debug info
    logger.info('Creating IP') # info for logfile
    
    # get current site_profile and zone
    site_profile, zone = getSiteZone()
    
    # get template files
    parameters = Parameter.objects.all()
    templatefile_log = parameters.get(entity="ip_logfile").value
    templatefile_cspec = parameters.get(entity="content_descriptionfile").value
    templatefile_pspec = parameters.get(entity="package_descriptionfile").value
    templatefile_prspec = parameters.get(entity="preservation_descriptionfile").value

    # get paths for different purposes
    env = Path.objects.get(entity='path_definitions').value
    destination_path = Path.objects.get(entity="path_preingest_reception").value
    source_path = ip.directory

    # NS definitions
    METS_NAMESPACE = SchemaProfile.objects.get(entity='mets_namespace').value
    METS_SCHEMALOCATION = SchemaProfile.objects.get(entity='mets_schemalocation').value
    XLINK_NAMESPACE = SchemaProfile.objects.get(entity='xlink_namespace').value
    XSI_NAMESPACE = SchemaProfile.objects.get(entity='xsi_namespace').value
    namespacedef = 'xmlns:mets="%s"' % METS_NAMESPACE
    namespacedef += ' xmlns:xlink="%s"' % XLINK_NAMESPACE
    namespacedef += ' xmlns:xsi="%s"' % XSI_NAMESPACE
    namespacedef += ' xsi:schemaLocation="%s %s"' % (METS_NAMESPACE, METS_SCHEMALOCATION)
    PREMIS_SCHEMALOCATION = SchemaProfile.objects.get(entity='premis_schemalocation').value
    

    # create IP for site profile SE and relevant zone
    if site_profile == 'SE' :

        checksumtype = 1 # MD5
        checksumalgoritm = 'MD5'
        path4m = ip.directory+'/'+ip.uuid+'/'+ 'metadata'
        #path4s = ip.directory+'/'+ip.uuid+'/'+ 'system'
        
        if zone == 'zone1':

            # METS records
            ObjectIdentifierValue = ip.uuid  
            #Cmets_objpath = destination_path+'/'+templatefile_cspec
            Cmets_objpath = ip.directory+'/'+ip.uuid+'/'+templatefile_cspec
            #METS_LABEL = contextdata['label']                   
            METS_LABEL = ip.label
            METS_PROFILE = SchemaProfile.objects.get(entity='mets_profile').value
            #METS_TYPE = 'SIP' 
            #METS_TYPE = contextdata['type']
            METS_TYPE = ip.iptype 
            METS_RECORDSTATUS = 'NEW'
            METS_DocumentID = templatefile_cspec
            TimeZone = 'Europe/Stockholm'

            # get agent lists
            agent_list = create_AgentList_SE(ip, contextdata)
            
            # get altRecordID lists
            altRecordID_list = create_altRecordIDList_SE(ip, contextdata)


    # create IP for site profile NO and relevant zone
    if site_profile == 'NO':

        checksumtype = 2 # SHA256
        checksumalgoritm = 'SHA-256'
        path4am = ip.directory+'/'+ip.uuid+'/'+ 'administrative_metadata'
        path4dm = ip.directory+'/'+ip.uuid+'/'+ 'descriptive_metadata'
        
        if zone == 'zone1':

            # NS definitions
            METS_SCHEMALOCATION_LOCAL = SchemaProfile.objects.get(entity='mets_schemalocation_local').value
            namespacedeflocal = 'xmlns:mets="%s"' % METS_NAMESPACE
            namespacedeflocal += ' xmlns:xlink="%s"' % XLINK_NAMESPACE
            namespacedeflocal += ' xmlns:xsi="%s"' % XSI_NAMESPACE
            namespacedeflocal += ' xsi:schemaLocation="%s %s"' % (METS_NAMESPACE, METS_SCHEMALOCATION_LOCAL)
            
            # METS records
            ObjectIdentifierValue = ip.uuid  
            #Cmets_objpath = destination_path+'/'+templatefile_spec
            Cmets_objpath = ip.directory+'/'+ip.uuid+'/'+templatefile_cspec
            #METS_LABEL = contextdata['label']                   
            METS_LABEL = ip.label
            METS_PROFILE = SchemaProfile.objects.get(entity='mets_profile').value
            #METS_TYPE = 'SIP' 
            #METS_TYPE = contextdata['type']
            METS_TYPE = ip.iptype 
            METS_RECORDSTATUS = 'NEW'
            METS_DocumentID = templatefile_cspec
            TimeZone = 'Europe/Stockholm'
        
            # get agent lists
            #agent_list_info, agent_list_mets = create_AgentList_NO(ip, contextdata)
            agent_list_info, agent_list_mets = create_AgentList_EC(ip, contextdata)
            
            # get altRecordID lists
            #altRecordID_list_info, altRecordID_list_mets = create_altRecordIDList_NO(ip, contextdata)
            altRecordID_list_info, altRecordID_list_mets = create_altRecordIDList_EC(ip, contextdata)

    # If platform is windows check if any file still is open
    if platform.system() != 'Linux' :
        sourceroot = ip.directory+'/'+ip.uuid
        for dirname, dirnames, filenames in os.walk( sourceroot ):
            for fil in filenames:
                file_name = os.path.join(dirname, fil)
                status = FileLock(fname=file_name,timeout=5).is_locked()
                if status :
                    logger.error('We have a locked file %s in IP %s' % (sourceroot, file_name))
                    return ip, status, 'We have a locked file %s in IP %s' % (file_name, sourceroot)
        logger.info('We have a no locked files in IP %s' % sourceroot)


    # copy public or local premis xsd-file to IP directory
    logger.info('Copy PREMIS xsd file')
    if site_profile == 'SE':
        schema = PREMIS_SCHEMALOCATION
        xsdpath = path4m  # could also be path4s
    if site_profile == 'NO':
        schema = PREMIS_SCHEMALOCATION
        xsdpath = path4am  # could also be path4dm
    filename, status, why = copy_Schema(xsdpath,schema,env)
    if status:
        if status == 1 :
            logger.error('The server could not fulfill the request. File: %s Error code: %s ' % (filename, why))
            return ip, status, why
        if status == 2:
            logger.error('We failed to reach the server. File: %s Reason: %s' % (filename, why))
            return ip, status, why
        if status == 3:
            logger.info('Successfully saved XSD-file %s', filename)
        if status == 4:
            logger.info('Successfully copied XSD-file %s', filename)
   
    #print 'Premis file %s' % filename

    # copy public or local inner mets xsd-file to IP directory
    logger.info('Copy METS xsd file')
    if site_profile == 'SE':
        schema = METS_SCHEMALOCATION
        xsdpath = path4m
    if site_profile == 'NO':
        schema = METS_SCHEMALOCATION_LOCAL
        #xsdpath = ObjectPath
        xsdpath = ip.directory+'/'+ip.uuid
    filename, status, why = copy_Schema(xsdpath,schema,env)
    if status:
        if status == 1 :
            logger.error('The server could not fulfill the request. File: %s Error code: %s ' % (filename, why))
            return ip, status, why
        if status == 2:
            logger.error('We failed to reach the server. File: %s Reason: %s' % (filename, why))
            return ip, status, why
        if status == 3:
            logger.info('Successfully saved XSD-file %s', filename)
        if status == 4:
            logger.info('Successfully copied XSD-file %s', filename)


    # create PREMIS-file and add it to METS-file amdSec
    logger.info('Create PREMIS xml file')
    #Premis_ObjectPath = ObjectPath+'/'+templatefile_prspec
    ms_files = [] # a new initial empty list
    ObjectPath = ip.directory+'/'+ip.uuid
    if site_profile == 'SE':
        Premis_ObjectPath = path4m + '/' + templatefile_prspec
    if site_profile == 'NO':
        Premis_ObjectPath = path4am + '/' + templatefile_prspec
    ms_files, status, errno, why = create_PremisFile(ip, ms_files, ObjectPath, Premis_ObjectPath, ObjectIdentifierValue, checksumalgoritm, checksumtype)
    if errno:
        logger.error('Could not create Premis file %s Reason: %s', Premis_ObjectPath, why)
        return ip, errno, why
    #else:
    #    logger.info('Successfully created Premis file %s', Premis_ObjectPath)

    # Depending on site profile use local or public schema for mets.xml and mets.xsd
    if site_profile == 'SE':
        namespaces = namespacedef  # If site profile is SE use public schema for mets.xml
    if site_profile == 'NO':
        namespaces = namespacedeflocal  # If site profile is NO use local schema for mets.xml
        agent_list = agent_list_mets
        altRecordID_list = altRecordID_list_mets

    # create inner mets-file if it does not exist
    logger.info('Create METS xml file')
    #ms_files = CreateMetsStructmap(site_profile, ms_files, TimeZone, ObjectPath, checksumtype, checksumalgoritm )
    if not os.path.isfile(Cmets_objpath):
        ESSMD.Create_IP_mets(ObjectIdentifierValue = ObjectIdentifierValue,
                                 METS_ObjectPath = Cmets_objpath,
                                 agent_list = agent_list,
                                 altRecordID_list = altRecordID_list,
                                 file_list = ms_files,
                                 namespacedef = namespaces,
                                 METS_LABEL = METS_LABEL,
                                 METS_PROFILE = METS_PROFILE,
                                 METS_TYPE = METS_TYPE,
                                 METS_RECORDSTATUS = METS_RECORDSTATUS,
                                 METS_DocumentID = METS_DocumentID,
                                 TimeZone = TimeZone)
        logger.info('Successfully created content description file %s for IP %s', Cmets_objpath, ip.label)
    else:
        logger.error('Content description file %s already exist', Cmets_objpath)

    
    # Validate inner mets-file
    logger.info('Validate METS xml file')
    errno, why = validate(FILENAME=Cmets_objpath)
    if errno:
        logger.error('Could not validate content description file %s Reason: %s', Cmets_objpath, why)
        return ip, errno, why
    else:
        logger.info('Successfully validated content description file %s', Cmets_objpath)

            
    # validate logical and physical representation of objects
    logger.info('Diffcheck inner METS xml file') 
    checksumtype_default = checksumalgoritm
    METS_ObjectPath = Cmets_objpath
    errno, result, reslist = DiffCheck_IP(ObjectIdentifierValue, ObjectPath, METS_ObjectPath, TimeZone, checksumtype_default)
    result_sum = len(reslist[0]) + len(reslist[1]) + len(reslist[2]) + len(reslist[3]) + len(reslist[4]) + len(reslist[5])
    if result_sum != len(reslist[0]):
        result[0].append("We have a mismatch !!!")
        errno = 1
        return ip, errno, result[0] 
    else:
        logger.info('Physical files match the logical representation of content description file %s', METS_ObjectPath)


    # Create a new information package folder ready for deliver
    i = 1
    while os.path.exists( os.path.join( destination_path, "ip%d"%i ) ):
        i+=1
    delivery_root = os.path.join( destination_path, "ip%d"%i )
    os.makedirs( delivery_root )


    # create IP tar file 
    ip_file = os.path.join(delivery_root, ip.uuid)
    root_dir = ip.directory
    base_dir = ip.uuid
    shutil.make_archive(ip_file, 'tar', root_dir, base_dir)
    logger.info('Successfully created IP tar file %s.tar', ip_file)


    # If site profile is NO use external schema for info.xml
    if site_profile == 'NO':
        namespaces = namespacedef
        agent_list = agent_list_info
        altRecordID_list = altRecordID_list_info

    
    # create outer mets-file file format = tar etc
    logger.info('Create outer METS xml file')
    templatefile_spec = templatefile_pspec
    METS_DocumentID = templatefile_spec
    ObjectPath = delivery_root
    mets_objpath = delivery_root+'/'+templatefile_spec
    ms_files = [] # a new empty list for outer mets-file
    ms_files = CreateMetsStructmap(site_profile, ms_files, TimeZone, ObjectPath, checksumtype, checksumalgoritm )
    if not os.path.isfile(mets_objpath):
        ESSMD.Create_IP_mets(ObjectIdentifierValue = ObjectIdentifierValue,
                                   METS_ObjectPath = mets_objpath,
                                   agent_list = agent_list,
                                   altRecordID_list = altRecordID_list,
                                   file_list = ms_files,
                                   namespacedef = namespaces,
                                   METS_LABEL = METS_LABEL,
                                   METS_PROFILE = METS_PROFILE,
                                   METS_TYPE = METS_TYPE,
                                   METS_RECORDSTATUS = METS_RECORDSTATUS,
                                   METS_DocumentID = METS_DocumentID,
                                   TimeZone = TimeZone)
        logger.info('Successfully created package description file %s for IP tar file %s', mets_objpath, ip_file)
    else:
        logger.error('Package description file %s already exist', mets_objpath)

                                        
    # Validate outer mets-file
    logger.info('Validate outer METS xml file')
    errno, why = validate(FILENAME=mets_objpath)
    if errno:
        return ip, errno, why
    else:
        logger.info('Successfully validated package description file %s', mets_objpath)

    
    # validate logical and physical representation of objects
    logger.info('Diffcheck outer METS xml file')
    checksumtype_default = checksumalgoritm
    METS_ObjectPath = mets_objpath
    errno, result, reslist = DiffCheck_IP(ObjectIdentifierValue, ObjectPath, METS_ObjectPath, TimeZone, checksumtype_default)
    result_sum = len(reslist[0]) + len(reslist[1]) + len(reslist[2]) + len(reslist[3]) + len(reslist[4]) + len(reslist[5])
    if result_sum != len(reslist[0]):
        result[0].append("We have a mismatch !!!")
        return ip, errno, result[0] 
    else:
        logger.info('Physical files match the logical representation of package description file %s', METS_ObjectPath)

    
    # Remove source ip directory and all files in it
    while True:
        try:
            #print ip.directory
            shutil.rmtree(ip.directory)
            break
        except:
            time.sleep(1)

        
    # mark IP as created and new directory
    ip.state = "Created"
    ip.directory = delivery_root 
    ip.progress = 100
    ip.save()

    return ip, 0, "Ok"



###############################################
"Copy XML-Schema"
"""
ET090 - BS130301 - Ready for test
ET091 - BS130324 - Wrapped in get_URL() and changed return value strings
"""
def copy_Schema( xsdpath, schema, env ):
    version = 'ET091'
    logger.debug('%s Entered copy_Schema' % version) # debug info
        
    # keep track of error descriptions etc
    status_list = []
    status = 0 
    
    #filename = ip.directory + '/' + ip.uuid + '/' + schema.split('/')[-1]
    filename = xsdpath + '/' + schema.split('/')[-1]
    if schema.split('/')[0] == 'http:':
        try:
            response = urlopen(Request(schema), timeout=5)
        except HTTPError as e:
            status = 1
            return filename, status, e.code
        except URLError as e:
            status = 2
            return filename, status, e.reason
        else:
            status = 3
            context = response.read()
            f_name = open( filename, "w" )
            f_name.write( context )
            f_name.close()
            return filename, status, context
    else:
        status = 4
        src_file = env + '/' + schema.split('/')[-1] 
        dst_file = filename
        shutil.copy(src_file, dst_file)

    return filename, status, status_list



###############################################
"Get URL data"
"""
ET090 - BS130301 - Ready for test
ET091 - BS130324 - Changed return value strings
"""
def get_URL(url):
    version = 'ET091'
    logger.debug('%s Entered get_URL' % version) # debug info

    errno = 0
    req = Request(url)
    try:
        response = urlopen(req, timeout=5)
    except HTTPError as e:
        errno = 1
        logger.error('The server could not fulfill the request. Error code: %s ' % e.code)
        return errno, e.code
    except URLError as e:
        errno = 2
        logger.error('We failed to reach the server. Reason: %s' % e.reason)
        return errno, e.reason
    else:
        context = response.read()
        return errno, context

        #url = response.geturl() # get url
        #filename = url.split('/')[-1] # get filename in url
        

###############################################
"Diffcheck"
"""
ET090 - BS130301 - Ready for test
"""
def DiffCheck_IP(ObjectIdentifierValue,ObjectPath,METS_ObjectPath=None,TimeZone='Europe/Stockholm',checksumtype_default='MD5'):  
    version = 'ET090'
    logger.debug('%s Entered DiffCheck_IP' % version) # debug info

    status_code = 0
    status_list = []
    error_list = []
    res_list = []
    errno = 0 

    ObjectPath = ObjectPath
    if METS_ObjectPath is None:
        Cmets_obj = 'sip.xml'
        Cmets_objpath = os.path.join(ObjectPath,Cmets_obj)
    else:
        Cmets_objpath = METS_ObjectPath
        Cmets_obj = os.path.split(Cmets_objpath)[1]
    ObjectIdentifierValue = ObjectIdentifierValue
    
    if status_code == 0:
        ###########################################################
        # get object_list from METS 
        res_info, res_files, res_struct, errno, why = getMETSFileList(FILENAME=Cmets_objpath)
        if not errno == 0:
            event_info = 'Problem to get object_list from METS for information package: %s, errno: %s, detail: %s' % (ObjectIdentifierValue,str(errno),str(why))
            error_list.append(event_info)
            status_code = 1
    if status_code == 0:
        ###########################################################
        # Insert METS file as first object in IP package
        M_CHECKSUM = utils.calcsum(Cmets_objpath,checksumtype_default)
        M_statinfo = os.stat(Cmets_objpath)
        M_SIZE = M_statinfo.st_size
        M_utc_mtime = datetime.datetime.utcfromtimestamp(M_statinfo.st_mtime).replace(tzinfo=pytz.utc)
        M_lociso_mtime = M_utc_mtime.astimezone(pytz.timezone(TimeZone)).isoformat()
        res_files.insert(0,['amdSec', None, 'techMD', 'techMD001', None,
                                 None, 'ID%s' % str(uuid.uuid1()), 'URL', 'file:%s' % Cmets_obj, 'simple',
                                 M_CHECKSUM, checksumtype_default, M_SIZE, 'text/xml', M_lociso_mtime,
                                 #M_CHECKSUM, 'MD5', M_SIZE, 'text/xml', M_lociso_mtime,
                                 'OTHER', 'METS', None])
    if status_code == 0:
        # present is used to detect case changed files on Windows
        checksums = {} # Map fname->checksum
        checksums_algo = {} # Map fname->checksumtype
        present = {}   # Map checksum->fname for present files 
        deleted = {}   # Map checksum->fname for deleted files
        
        file_list = []
        changed = []   # Changed files
        added = []     # Added files
        confirmed = [] # Confirmed files
        renamed = []   # Renamed files as (old,new) pairs
        permission = [] # Permission problem
     
        result = ''           
        
        for object in res_files:
            ok = 1
            filepath = os.path.join(ObjectPath, object[8][5:])
            fname = object[8][5:]
            checksum = object[10]
            hash_algo = object[11].lower()
            #print 'filepath: %s, object: %s' % (self.filepath, str(self.object[11].lower()))
            if os.access(filepath,os.R_OK):
                checksums[fname] = checksum
                present[checksum] = fname
                if not os.access(filepath,os.W_OK):
                    permission.append(fname)
            else:
                deleted[checksum] = fname
            checksums_algo[fname] = hash_algo

        file_list, errno, why = GetFiletree2(ObjectPath, 2)
        #for fname in GetFiletree(ObjectPath):
        for fname in file_list:
            fname = fname[0]
            if fname not in checksums:
                if fname in checksums_algo:
                    checksumtype = checksums_algo[fname]
                else:
                    checksumtype = checksumtype_default
                newhash = utils.calcsum(os.path.join(ObjectPath,fname),checksumtype)
                checksums[fname] = newhash
                if newhash in deleted:
                    renamed.append((deleted[newhash], fname))
                    del deleted[newhash]
                elif newhash in present:
                    oldname = present[newhash]
                    if oldname.lower() == fname.lower():
                        renamed.append((oldname, fname))
                        del checksums[oldname]
                        checksums[fname] = newhash
                else:
                    added.append(fname)
            else:
                checksumtype = checksums_algo[fname]
                newhash = utils.calcsum(os.path.join(ObjectPath,fname),checksumtype)
                if checksums[fname] == newhash:
                    if not newhash in permission:
                        confirmed.append(fname)
                else:
                    changed.append(fname)

    if status_code == 0:
        # Log all changes
        #for fname in confirmed:
        #    result+="%s\n" % "CONFIRMED %s" % os.path.join(self.ObjectPath,fname) 
        for old, new in renamed:
            result+="%s\n" % "RENAMED %s: %s --> %s" % (ObjectPath,old,new)
            status_list.append("RENAMED %s: %s --> %s" % (ObjectPath,old,new)) 
        for fname in added:
            result+="%s\n" % "ADDED %s" % os.path.join(ObjectPath,fname)
            status_list.append("ADDED %s" % os.path.join(ObjectPath,fname))
        for fname in sorted(deleted.itervalues()):
            result+="%s\n" % "DELETED %s" % os.path.join(ObjectPath,fname)
            status_list.append("DELETED %s" % os.path.join(ObjectPath,fname))
        for fname in changed:
            result+="%s\n" % "CHANGED %s" % os.path.join(ObjectPath,fname)
            status_list.append("CHANGED %s" % os.path.join(ObjectPath,fname))
        for fname in permission:
            result+="%s\n" % "PERMISSION_ERROR %s" % os.path.join(ObjectPath,fname)
            status_list.append("PERMISSION_ERROR %s" % os.path.join(ObjectPath,fname))
        result+="%s\n" % "STATUS %s" % "confirmed %d renamed %d added %d deleted %d changed %d permission_error %d" % (
            len(confirmed), len(renamed), len(added), len(deleted), len(changed), len(permission))
        status_list.append("STATUS %s" % "confirmed %d renamed %d added %d deleted %d changed %d permission_error %d" % (
            len(confirmed), len(renamed), len(added), len(deleted), len(changed), len(permission)))
        res_list.append(confirmed)
        res_list.append(renamed)
        res_list.append(added)
        res_list.append(deleted)
        res_list.append(changed)
        res_list.append(permission)
         
    return status_code, [status_list,error_list], res_list    


###############################################
"Get file list from METS file"
"""
ET090 - BS130301 - Ready for test
"""
def getMETSFileList(DOC=None,SecTYPE=['ALL'],ID=['ALL'],USE=['ALL'],MIMETYPE=["ALL"],FILENAME=None):
    version = 'ET090'
    logger.debug('%s Entered getMETSFileList' % version) # debug info

    #MIMETYPE=["ALL","application/x-tar"]
    #USE=["ALL","PACKAGE"]
    #SecTYPE=["ALL","dmdSec","amdSec","fileSec"]
    #ID=["ALL","fgrp001","techMD001"]

    res = []
    Hdr_res = []
    if FILENAME:
        try:
            DOC  =  etree.ElementTree ( file=FILENAME )
        except etree.XMLSyntaxError, detail:
            return [],[],[],10,str(detail)
        except IOError, detail:
            return [],[],[],20,str(detail)

    EL_root = DOC.getroot()
    mets_NS = "{%s}" % EL_root.nsmap['mets']
    xlink_NS = "{%s}" % EL_root.nsmap['xlink']

    ###############################################
    # mets root
    a_LABEL = EL_root.get('LABEL')
    a_OBJID = EL_root.get('OBJID')
    a_PROFILE = EL_root.get('PROFILE')
    a_TYPE = EL_root.get('TYPE')
    a_ID = EL_root.get('ID')
    Hdr_res.append([a_LABEL,a_OBJID,a_PROFILE,a_TYPE,a_ID])

    ###############################################
    # metsHdr
    metsHdr = DOC.find("%smetsHdr" % mets_NS)
    a_CREATEDATE = metsHdr.get('CREATEDATE')
    metsDocumentID = metsHdr.find("%smetsDocumentID" % mets_NS)
    if metsDocumentID is not None:
        t_metsDocumentID = metsDocumentID.text
    else:
        t_metsDocumentID = None
    Hdr_res.append([a_CREATEDATE,t_metsDocumentID])
    agent_all = metsHdr.findall("%sagent" % mets_NS)
    agent_res = []
    for agent in agent_all:
        a_ROLE = agent.get('ROLE')
        a_OTHERROLE = agent.get('OTHERROLE')
        a_TYPE = agent.get('TYPE')
        a_OTHERTYPE = agent.get('OTHERTYPE')
        name = agent.find("%sname" % mets_NS)
        if name is not None:
            t_name = name.text
        else:
            t_name = None
        note_res = []
        note_all = agent.findall("%snote" % mets_NS)
        for note in note_all:
            t_note = note.text
            note_res.append(t_note)
        agent_res.append([a_ROLE,a_OTHERROLE,a_TYPE,a_OTHERTYPE,t_name,note_res])
    Hdr_res.append(agent_res)
    altRecordID_all = metsHdr.findall("%saltRecordID" % mets_NS)
    altRecordID_res = []
    for altRecordID in altRecordID_all:
        a_TYPE = altRecordID.get('TYPE')
        altRecordID_value = altRecordID.text
        altRecordID_res.append([a_TYPE,altRecordID_value])
    Hdr_res.append(altRecordID_res)
    
    if 'dmdSec' in SecTYPE or 'ALL' in SecTYPE:
        ###############################################
        # dmdSec
        Sec_NAME = 'dmdSec'
        dmdSec_all = DOC.findall("%sdmdSec[@ID]" % mets_NS)
        for dmdSec in dmdSec_all:
            Sec_ID = dmdSec.get("ID")
            Grp_NAME = None
            Grp_ID = None
            Grp_USE = None
            ###############################################
            # MD
            for md in getmd(dmdSec,Sec_NAME,Sec_ID,Grp_NAME,Grp_ID,Grp_USE):
                res.append(md)

    if 'amdSec' in SecTYPE or 'ALL' in SecTYPE:
        ###############################################
        # amdSec
        Sec_NAME = 'amdSec'
        amdSec_all = DOC.findall("%samdSec[@ID]" % mets_NS)
        for amdSec in amdSec_all:
            Sec_ID = amdSec.get("ID")
            ###############################################
            # techMD
            techMD_all = amdSec.findall("%stechMD[@ID]" % mets_NS)
            for techMD in techMD_all:
                Grp_NAME = 'techMD'
                Grp_ID = techMD.get("ID")
                Grp_USE = techMD.get("USE")
                if techMD.get("ID") in ID or 'ALL' in ID:
                    for md in getmd(techMD,Sec_NAME,Sec_ID,Grp_NAME,Grp_ID,Grp_USE):
                        res.append(md)    
            ###############################################
            # digiprovMD
            digiprovMD_all = amdSec.findall("%sdigiprovMD[@ID]" % mets_NS)
            for digiprovMD in digiprovMD_all:
                Grp_NAME = 'digiprovMD'
                Grp_ID = digiprovMD.get("ID")
                Grp_USE = digiprovMD.get("USE")
                if digiprovMD.get("ID") in ID or 'ALL' in ID:
                    for md in getmd(digiprovMD,Sec_NAME,Sec_ID,Grp_NAME,Grp_ID,Grp_USE):
                        res.append(md)

    if 'fileSec' in SecTYPE or 'ALL' in SecTYPE:
        ###############################################
        # fileSec
        Sec_NAME = 'fileSec'
        fileSec = DOC.find("%sfileSec" % mets_NS)
        Sec_ID = fileSec.get("ID")
        fileGrp_all = fileSec.findall("%sfileGrp" % mets_NS)
        for fileGrp in fileGrp_all:
            Grp_NAME = 'fileGrp'
            Grp_ID = fileGrp.get("ID")
            Grp_USE = fileGrp.get("USE")
            if fileGrp.get("ID") in ID or 'ALL' in ID:
                ###############################################
                # file
                md_type = 'file'
                file_all = fileGrp.findall("%sfile" % mets_NS)
                for EL_file in file_all:
                    if EL_file.get('USE') in USE or 'ALL' in USE and EL_file.get('MIMETYPE') in MIMETYPE or 'ALL' in MIMETYPE:
                        a_ID = EL_file.get('ID')
                        a_MIMETYPE = EL_file.get('MIMETYPE')
                        a_CREATED = EL_file.get('CREATED')
                        a_CHECKSUM = EL_file.get('CHECKSUM')
                        a_CHECKSUMTYPE = EL_file.get('CHECKSUMTYPE')
                        a_USE = EL_file.get('USE')
                        a_SIZE = int(EL_file.get('SIZE'))
                        a_ADMID = EL_file.get('ADMID')
                        a_DMDID = EL_file.get('DMDID')
                        EL_FLocat = EL_file.find("%sFLocat" % mets_NS)
                        a_LOCTYPE = EL_FLocat.get('LOCTYPE')
                        a_href = EL_FLocat.get('%shref' % xlink_NS)
                        #a_href = urllib.url2pathname(a_href).decode('utf-8')
                        a_href = utils.str2unicode(urllib.unquote(a_href))
                        a_type = EL_FLocat.get('%stype' % xlink_NS)
                        res.append([Sec_NAME,
                                    Sec_ID,
                                    Grp_NAME,
                                    Grp_ID,
                                    Grp_USE,
                                    md_type,
                                    a_ID,
                                    a_LOCTYPE,
                                    a_href,
                                    a_type,
                                    a_CHECKSUM,
                                    a_CHECKSUMTYPE,
                                    a_SIZE,
                                    a_MIMETYPE,
                                    a_CREATED,
                                    a_USE,
                                    a_ADMID,
                                    a_DMDID,
                        ])

    ###############################################
    # structMap
    structMap = DOC.find("%sstructMap" % mets_NS)
    
    a_LABEL = structMap.get("LABEL")
    struct_res = [a_LABEL, getdiv(structMap)]

    return Hdr_res, res,struct_res,0,None


###############################################
"XXX"
"""
ET090 - BS130301 - Ready for test
"""
def getdiv(EL):
    version = 'ET090'
    logger.debug('%s Entered getdiv' % version) # debug info
    
    mets_NS = "{%s}" % EL.nsmap['mets']
    xlink_NS = "{%s}" % EL.nsmap['xlink']
    res = []
    ###############################################
    # div
    div_all = EL.findall("%sdiv" % mets_NS)
    for div in div_all:
        a_FILEID = None
        a_LABEL = div.get('LABEL')
        a_ADMID = div.get('ADMID')
        a_DMDID = div.get('DMDID')
        EL_fptr_all = div.findall("%sfptr" % mets_NS)
        if len(EL_fptr_all):
            for EL_fptr in EL_fptr_all:
                a_FILEID = EL_fptr.get('FILEID')
                res.append([a_LABEL, a_ADMID, a_DMDID, a_FILEID])
        else:
            res.append([a_LABEL, a_ADMID, a_DMDID, a_FILEID])
        newdata = getdiv(div)
        if len(newdata):
            res.append(newdata)
    return res


###############################################
"XX"
"""
ET090 - BS130301 - Ready for test
"""
def getmd(EL,Sec_NAME,Sec_ID,Grp_NAME,Grp_ID,Grp_USE):
    version = 'ET090'
    logger.debug('%s Entered getmd' % version) # debug info
    
    mets_NS = "{%s}" % EL.nsmap['mets']
    xlink_NS = "{%s}" % EL.nsmap['xlink']
    res = []

    ###############################################
    # mdRef
    mdRef_all = EL.findall("%smdRef" % mets_NS)
    md_type = 'mdRef'
    for mdRef in mdRef_all:
        a_CREATED = mdRef.get('CREATED')
        a_MDTYPE = mdRef.get('MDTYPE')
        a_OTHERMDTYPE = mdRef.get('OTHERMDTYPE')
        a_ID = mdRef.get('ID')
        a_SIZE = int(mdRef.get('SIZE'))
        a_MIMETYPE = mdRef.get('MIMETYPE')
        a_CHECKSUMTYPE = mdRef.get('CHECKSUMTYPE')
        a_CHECKSUM = mdRef.get('CHECKSUM')
        a_LOCTYPE = mdRef.get('LOCTYPE')
        a_href = mdRef.get('%shref' % xlink_NS)
        a_type = mdRef.get('%stype' % xlink_NS)
        res.append([Sec_NAME,
                    Sec_ID,
                    Grp_NAME,
                    Grp_ID,
                    Grp_USE,
                    md_type,
                    a_ID,
                    a_LOCTYPE,
                    a_href,
                    a_type,
                    a_CHECKSUM,
                    a_CHECKSUMTYPE,
                    a_SIZE,
                    a_MIMETYPE,
                    a_CREATED,
                    a_MDTYPE,
                    a_OTHERMDTYPE,
                    ])

        ###############################################
        # mdWrap
        mdWrap_all = EL.findall("%smdWrap" % mets_NS)
        md_type = 'mdWrap'
        for mdWrap in mdWrap_all:
            a_MDTYPE = mdWrap.get('MDTYPE')
            a_OTHERMDTYPE = mdWrap.get('OTHERMDTYPE')
            binData = mdWrap.find("%sbinData" % mets_NS)
            xmlData = mdWrap.find("%sxmlData" % mets_NS)
            if binData is not None:
                mdWrap_type = 'binData'
                mdWrap_data = binData
            elif xmlData is not None:
                mdWrap_type = 'xmlData'
                mdWrap_data = xmlData
            else:
                mdWrap_type = None
                mdWrap_data = None
            res.append([Sec_NAME,
                        Sec_ID,
                        Grp_NAME,
                        Grp_ID,
                        Grp_USE,
                        md_type,
                        mdWrap_type,
                        mdWrap_data,
                        a_MDTYPE,
                        a_OTHERMDTYPE,
                        ])
    
    return res



###############################################
"Create amdSec / structMap / fileSec"
"""
ET090 - BS130301 - Ready for test
"""
def CreateMetsStructmap(site_profile, ms_files, TimeZone, ObjectPath, checksumtype, checksumalgoritm ):
    version = 'ET090'
    logger.debug('%s Entered CreateMetsStructmap' % version) # debug info
    
    # get template files
    parameters = Parameter.objects.all()
    templatefile_cspec = parameters.get(entity="content_descriptionfile").value
    templatefile_pspec = parameters.get(entity="package_descriptionfile").value
    templatefile_prspec = parameters.get(entity="preservation_descriptionfile").value
    templatefile_log = parameters.get(entity="ip_logfile").value

    logfile_exist = 0
    for i in ms_files:
        #print i[8][5:]
        if i[8][5:] == templatefile_log:
            logfile_exist = 1
            break 
        
        
        
    # find out path for metadata
    if site_profile == 'SE':    
        path4m = 'metadata/'
        #print path4m
    if site_profile == 'NO':
        path4m = 'administrative_metadata/'
        #print path4m
    # create filetree to read
    if not len(ms_files):      
        ms_files = []
    if ObjectPath is not None:
        Filetree_list, errno, why = GetFiletree2(ObjectPath,checksumtype)
        if not errno:
            for f in Filetree_list:
                f_name = f[0]
                f_size = f[1].st_size
                f_created = datetime.datetime.fromtimestamp(f[1].st_mtime,pytz.timezone(TimeZone)).replace(microsecond=0).isoformat()
                f_checksum = f[2]
                f_mimetype = f[3]
                #print 'filename: %s, size: %s, created: %s, checksum: %s, mimetype: %s' % (f_name,f_size,f_created,f_checksum,f_mimetype)

                # Don't add log file if already exist
                if f_name == templatefile_log and logfile_exist:
                    continue
                    
                # Don't add preservation file
                #print ObjectPath.split('/')
                if f_name == path4m + templatefile_prspec:
                    continue
                # Don't add delivery spec file
                if f_name == templatefile_pspec:
                    continue
                # Don't add content spec file
                if f_name == templatefile_cspec:
                    continue
                
                #if f_name[-10:] == 'premis.xml':
                #    ms_files.append(['amdSec', None, 'digiprovMD', 'digiprovMD001', None,
                #                     None, 'ID%s' % str(uuid.uuid1()), 'URL', 'file:%s' % f_name, 'simple',
                #                     f_checksum, checksumalgoritm, f_size, 'text/xml', f_created,
                #                     'PREMIS', None, None])
                else:
                    ms_files.append(['fileSec', None, None, None, None,
                                          None, 'ID%s' % str(uuid.uuid1()), 'URL', 'file:%s' % f_name, 'simple',
                                          f_checksum, checksumalgoritm, f_size, f_mimetype, f_created,
                                          'Datafile', None, None])
                                        #'Datafile', 'digiprovMD001', None])

                # ms_files example
                #ms_files.append([Sec_NAME, Sec_ID, Grp_NAME, Grp_ID, Grp_USE,
                #                 md_type, a_ID, a_LOCTYPE, a_href, a_type,
                #                 a_CHECKSUM, a_CHECKSUMTYPE, a_SIZE, a_MIMETYPE, a_CREATED,
                #                 a_MDTYPE/a_USE, a_OTHERMDTYPE/a_ADMID, a_DMDID])
        else:
            #logging.error('Problem to get filelist from objectpath: %s, errno: %s, why: %s' % (ObjectPath,errno,str(why)))
            status_code = 1

    #print ObjectPath, Filetree_list, ms_files
    #return ms_files, errno, why
    return ms_files



###############################################
"Get current site_profile and zone"
"""
ET090 - BS130301 - Ready for test
"""
def getSiteZone():
    version = 'ET090'
    logger.debug('%s Entered getSiteZone' % version) # debug info
    
    # find out which zone, if none set it to zone1
    try:
        zone = Parameter.objects.get(entity="zone").value
        if zone != "zone1" and zone != "zone2" and zone != "zone3" :  
            zone = "zone1"
    except:
        zone = "zone1"

    # find out which site_profile, if none set it to SE
    try:
        site_profile = Parameter.objects.get(entity="site_profile").value
        if site_profile != "SE" and site_profile != "NO" :
            site_profile = "SE"
    except:
        site_profile = "SE"

    return site_profile, zone


###############################################
"Create PREMIS-file"
"""
ET090 - BS130301 - Ready for test
"""
def create_PremisFile(ip, ms_files, ObjectPath, PREMIS_ObjectPath, ObjectIdentifierValue, checksumalgoritm, checksumtype):
    version = 'ET090'
    logger.debug('%s Entered create_PremisFile' % version) # debug info
    
    status_list = []
    error_list = []
    status_code = 0

    # get or set different variables
    site_profile, zone = getSiteZone()
    TimeZone = 'Europe/Stockholm'
    system = 'ESSArch'
    application = 'ESSArch Tools'
    IPTYPE = ip.iptype
    identifiertype = '%s/RA' % site_profile
    #ms_files, errno, why = CreateMetsStructmap(site_profile, ms_files, TimeZone, ObjectPath, checksumtype, checksumalgoritm )
    ms_files = CreateMetsStructmap(site_profile, ms_files, TimeZone, ObjectPath, checksumtype, checksumalgoritm )

######    
#    if errno:
#        error_list.append(why)
#        logger.error(why)
#        return ms_files, status_list, status_code, error_list
    
    # Create PREMISfile etc
    if PREMIS_ObjectPath is not None:
        status_list.append('Create new PREMIS: %s' % PREMIS_ObjectPath)
        P_ObjectIdentifierValue = ObjectIdentifierValue
        P_preservationLevelValue = 'full'
        P_compositionLevel = '0'
        P_formatName = 'tar'
        xml_PREMIS = ESSMD.createPremis(FILE=['simple','',identifiertype,P_ObjectIdentifierValue,P_preservationLevelValue,[],P_compositionLevel,P_formatName,'',application,[]])
        for res_file in ms_files:
            if res_file[0] == 'fileSec':
                F_objectIdentifierValue = '%s/%s' % (ObjectIdentifierValue,res_file[8][5:])
                F_messageDigest = res_file[10]
                F_messageDigestAlgorithm = res_file[11]
                F_size = str(res_file[12])
                F_formatName = res_file[13]
                F_formatName = ESSPGM.Check().MIMEtype2PREMISformat(res_file[13])
                xml_PREMIS = ESSMD.AddPremisFileObject(DOC=xml_PREMIS,FILES=[('simple','',identifiertype,F_objectIdentifierValue,'',[],'0',[[F_messageDigestAlgorithm,F_messageDigest,'ESSArch']],F_size,F_formatName,'',[],[['simple','',IPTYPE,P_ObjectIdentifierValue,'']],[['structural','is part of',identifiertype,P_ObjectIdentifierValue]])])

        # add agent to Premis file
        xml_PREMIS = ESSMD.AddPremisAgent(xml_PREMIS,[(identifiertype,system,application,'software')])

        # validate Premis file
        errno,why = validate(xml_PREMIS)
        if errno:
            status_code = 2
            error_list.append('Problem to validate "PREMISfile: %s", errno: %s, why: %s' % (PREMIS_ObjectPath,errno,str(why)))
            logger.error('Problem to validate "PREMISfile: %s", errno: %s, why: %s' % (PREMIS_ObjectPath,errno,str(why)))
        
        # create Premis file 
        errno,why = writeToFile(xml_PREMIS,PREMIS_ObjectPath)
        if errno:
            status_code = 3
            error_list.append('Problem to write "PREMISfile: %s", errno: %s, why: %s' % (PREMIS_ObjectPath,errno,str(why)))
            logger.error('Problem to write "PREMISfile: %s", errno: %s, why: %s' % (PREMIS_ObjectPath,errno,str(why)))
        else:
            logger.info('Successfully created and validated Premis file %s' % PREMIS_ObjectPath )
        
        # Add PREMISfile to METS filelist
        f_name = PREMIS_ObjectPath.replace( ObjectPath + '/', '' )
        f_stat = os.stat(PREMIS_ObjectPath)
        f_size = f_stat.st_size
        f_created = datetime.datetime.fromtimestamp(f_stat.st_mtime,pytz.timezone(TimeZone)).replace(microsecond=0).isoformat()
        f_checksum = utils.calcsum(PREMIS_ObjectPath, checksumalgoritm)
        f_mimetype = 'text/xml'
        ms_files.append(['amdSec', None, 'digiprovMD', 'digiprovMD001', None,
                         None, 'ID%s' % str(uuid.uuid1()), 'URL', 'file:%s' % f_name, 'simple',
                         f_checksum, checksumalgoritm, f_size, 'text/xml', f_created,
                         'PREMIS', None, None,
                         ])

    return ms_files, status_list, status_code, error_list


###############################################
"Get log metadata from logfile"
"""
ET090 - BS130301 - Ready for test
"""
def getLogMetadata( filename ):
    version = 'ET090'
    logger.debug('%s Entered getLogMetadata' % version) # debug info
    
    # Pull out the log file PREMIS metadata using a simple state-machine
    # approach, searching for the following tags:
    #  - objectIdentifierValue 
    #  - significantPropertiesType / significantPropertiesValue 
    significantPropertiesType=""
    significantPropertiesValue=""

    metadata = {}
    for event, element in etree.iterparse( filename ):
        if element.tag.endswith( "objectIdentifierValue" ):
            metadata[ "uuid" ] = element.text
        elif element.tag.endswith( "significantPropertiesType" ):
            significantPropertiesType=element.text
        elif element.tag.endswith( "significantPropertiesValue" ):
            significantPropertiesValue=element.text
        elif element.tag.endswith( "significantProperties" ):
            # end of significantProperties group, let's see if we have some data to work with:
            if significantPropertiesType!="" and significantPropertiesValue!="":
                metadata[ significantPropertiesType ] = significantPropertiesValue
                significantPropertiesType=""
                significantPropertiesValue=""
    #print metadata
    return metadata


###############################################
"Get logevents from logfile"
"""
ET090 - BS130301 - Ready for test
"""
def getLogEvents( filename ):
    version = 'ET090'
    logger.debug('%s Entered getLogEvents' % version) # debug info
    
    # Pull out the log file PREMIS metadata using a simple state-machine
    # approach, searching for specified tags:
    tags = [ "eventType", "eventDateTime", "eventDetail",
             "eventOutcome", "eventOutcomeDetailNote", 
             "linkingAgentIdentifierValue", "linkingObjectIdentifierValue" ]

    significantPropertiesType=""
    significantPropertiesValue=""

    tmpdata = {}
    logdata = []
    
    context = etree.iterparse( filename )
    
    for event, element in context:
        if element.tag.endswith( "event" ):
                # we have a complete event, add it to log data.
                logdata.append( tmpdata )
                tmpdata = {}
        else:
                for tag in tags:
                    if element.tag.endswith( tag ):
                            if tag == 'eventOutcome' and element.text == '0':
                                tmpdata[ tag ] = "Ok"
                            elif tag == 'eventOutcome' and element.text == '1':
                                tmpdata[ tag ] = "Failed"
                            else:
                                tmpdata[ tag ] = element.text
                            #print element.tag, element.text
                            #print '%s' % logdata
        
    return logdata


###############################################
"Get path to logfile"
"""
ET090 - BS130301 - Ready for test
"""
def getLogFilePath():
    version = 'ET090'
    logger.debug('%s Entered getLogFilePath' % version) # debug info
    
    # find out path to logfile
    # get current site_profile and zone
    site_profile, zone = getSiteZone()
    
    # check which source directory to use 
    if zone == 'zone1' :
        logfilepath = Path.objects.get(entity="path_preingest_prepare").value
    if zone == 'zone2' :
        #logfilepath = Path.objects.get(entity="path_gate").value+"/logs"
        #logfilepath = Path.objects.get(entity="path_gate").value+"/lobby"
        logfilepath = Path.objects.get(entity="path_gate").value
    if zone == 'zone3' :
        logfilepath = Path.objects.get(entity="path_work").value
    
    return logfilepath



###############################################
"Check log metadata"
"""
ET090 - BS130301 - Ready for test
"""
def checkLogMetadata(loglist):
    version = 'ET090'
    logger.debug('%s Entered checkLogMetdata' % version) # debug info
    
    # expected tags in logfile 
    tags = {'uuid',
            'archivist_organization',
            'label',
            #'startdate',
            #'enddate',
            'iptype',
            'createdate',
            }
    
    errno = 0
    diff_list = []
    for elem in tags:
        if elem not in loglist:
            diff_list.append(elem)
    if len(diff_list) != 0:
        errno=1
        status = "Mismatch between log elements"
    else:
        status = "Matches"
    return errno, status


###############################################
"Get spec files"
"""
ET090 - BS130301 - Ready for test
"""
def getFiles(sourceroot, filename):
    version = 'ET090'
    logger.debug('%s Entered getFiles' % version) # debug info
    
    # iterate through the directory structures looking for spec files,
    # load the spec file and extract metadata.
    
    files = []
    errno = 0
    for dirname, dirnames, filenames in os.walk( sourceroot ):
        #print dirname, dirnames, filenames
        for file in filenames:
            if file==filename:
                fullpath = os.path.join( dirname, file )
                metadata = ParseSpecFile( fullpath )
                #print metadata
                #errno, why = checkLogMetadata(metadata)
                if not errno:
                    metadata[ "fullpath" ] = fullpath
                    metadata[ "iplocation" ] = os.path.split(fullpath)[0]
                    #print metadata
                    files.append( metadata )
                    while len(dirnames) > 0 :
                        del dirnames[0] # remove the first entry in the list of sub-directories  

    return files


###############################################
"Get logfiles"
"""
ET090 - BS130301 - Ready for test
"""
def getLogFiles(sourceroot, filename):
    version = 'ET090'
    logger.debug('%s Entered getLogFiles' % version) # debug info
    
    # iterate through the directory structures looking for log files,
    # load the log file and extract metadata.
    
    logs=[]

    for dirname, dirnames, filenames in os.walk( sourceroot ):
        for file in filenames:
            if file==filename:
                fullpath = os.path.join( dirname, file )
                metadata = getLogMetadata( fullpath )
                errno, why = checkLogMetadata(metadata)
                if not errno:
                    metadata[ "fullpath" ] = fullpath
                    metadata[ "iplocation" ] = os.path.split(dirname)[0]
                    logs.append( metadata )
                    while len(dirnames) > 0 :
                        del dirnames[0] # remove the first entry in the list of sub-directories  

    return logs


###############################################
"Append log event to logfile"
"""
ET090 - BS130301 - Ready for test
"""
def appendToLogFile( logfile, eventType, eventOutcome, eventOutcomeDetailNote, linkingAgentIdentifierValue, linkingObjectIdentifierValue ):
    version = 'ET090'
    logger.debug('%s Entered appendToLogFile' % version) # debug info
    
    # append event to logfile
    
    # get current site_profile and zone
    site_profile, zone = getSiteZone()

    # get logfile tree structure
    DOC = etree.ElementTree ( file=logfile )

    # create timestamp
    eventDateTime = utils.creation_time('Europe/Stockholm')
    
    # get eventDetail
    eventDetail=LogEvent.objects.filter( eventType=eventType )[0].eventDetail

    # create event_uuid
    event_uuid = str(uuid.uuid1())
    
    # add premis event to logfile
    xml_PREMIS = AddPremisEvent( DOC,
                                 [('%s/ESS' % site_profile,
                                   event_uuid,
                                   eventType,
                                   eventDateTime,
                                   eventDetail,
                                   "%d" % eventOutcome,
                                   eventOutcomeDetailNote,
                                   [['%s/ESS' % site_profile,linkingAgentIdentifierValue]],
                                   [['%s/ESS' % site_profile,linkingObjectIdentifierValue]]
                                   )]
                                )

    writeToFile(xml_PREMIS,logfile)


###############################################    
"Create AIC directory"
"""
ET090 - BS130301 - Ready for test
"""
def createAICdirectory(sourceroot, aicuuid):
    version = 'ET090'
    logger.debug('%s Entered createAICdirectory' % version) # debug info
    
    # create AIC_UUID directory
    aicroot = os.path.join( sourceroot, aicuuid )
    os.makedirs( aicroot )
    
    return aicroot


###############################################
"Create IP directory"
"""
ET090 - BS130301 - Ready for test
"""
def createIPdirectory(sourceroot, ip_uuid):
    version = 'ET090'
    logger.debug('%s Entered createIPdirectory' % version) # debug info
    
    # get current site_profile and zone
    site_profile, zone = getSiteZone()

    # create IP_UUID directory
    iproot = os.path.join( sourceroot, ip_uuid )
    os.makedirs( iproot )

    # create subfolders to UUID folder
    if site_profile == "SE":
        os.makedirs( os.path.join( iproot, "content" ) )
        #os.makedirs( os.path.join( iproot, "Document" ) )
        os.makedirs( os.path.join( iproot, "metadata" ) )
        #os.makedirs( os.path.join( iproot, "system" ) )
    elif site_profile == "NO":
        os.makedirs( os.path.join( iproot, "descriptive_metadata" ) )
        os.makedirs( os.path.join( iproot, "administrative_metadata" ) )
        if zone == 'zone2':
            os.makedirs( os.path.join( os.path.join( iproot, "administrative_metadata" ), "repository_operations" ) )
        os.makedirs( os.path.join( iproot, "content" ) )
        # Removed 130323 by request from NRA
        #os.makedirs( os.path.join( os.path.join( iproot, "content" ), "documents" ) )

    return iproot
    

###############################################
"Parse specification file"
"""
ET090 - BS130301 - Ready for test
"""
def ParseSpecFile(filename):
    version = 'ET090'
    logger.debug('%s Entered ParseSpecFile' % version) # debug info
    
    # only parse start and end elements
    events = ('start', 'end', )
        
    # declare variables
    root = None
    metadata = {} 
        
    # iterparse xml file
    context = etree.iterparse( filename, events=events)
    
    # get metadata in xml file
    for event, elem in context:
            
        ##########################################        
        # separate namespace from tag
        namespace, tag = elem.tag[1:].split('}', 1)
            
        ##########################################
        # get root elements metadata
        if event == 'start' and root is None:
            root = elem.tag
            #contextdata["ip_uuid"] = context[0][4]
            metadata["ip_label"] = elem.get('LABEL')
            metadata["ip_uuid"] = elem.get('OBJID')
            metadata["ip_type"] = elem.get('TYPE')
            utils.clearNode(elem)
    
        ##########################################
        # get metsHdr element metadata
        if event == 'start' and tag == 'metsHdr' :
            metadata["ip_createdate"] = elem.get('CREATEDATE')
            utils.clearNode(elem)
                
        ##########################################
        # get agent elements metadata
        if event == 'end' and tag == 'agent' :
            m_ROLE = elem.get('ROLE')
            m_TYPE = elem.get('TYPE')
            m_OTHERTYPE = elem.get('OTHERTYPE')
            if m_ROLE == 'ARCHIVIST' and m_TYPE == 'ORGANIZATION':
                metadata["ip_archivist_organization"] = elem[0].text
#            if m_ROLE == 'CREATOR' and m_TYPE == 'ORGANIZATION':
#                metadata["ip_creator"] = elem[0].text
            #if m_ROLE == 'ARCHIVIST' and m_OTHERTYPE == 'SOFTWARE' :
            #    metadata["ip_system"] = elem[0].text
            #    metadata["ip_version"] = elem[1].text
            utils.clearNode(elem)
        
        ##########################################
        # get altrecordid elements metadata
        if event == 'end' and tag == 'altRecordID' :
            m_TYPE = elem.get('TYPE')
            #print elem.text
            if m_TYPE == 'STARTDATE' :
                metadata["ip_startdate"] = elem.text
            if m_TYPE == 'ENDDATE' :
                metadata["ip_enddate"] = elem.text
            utils.clearNode(elem)
            
    # remove context from memory
    del context

    return metadata


###############################################
"Add PREMIS event to log file"
"""
ET090 - BS130301 - Ready for test
"""
def AddPremisEvent(DOC=None,EVENTS=[('SE/RA','GUID123xasd','TIFF editering','2005-11-08 12:24:09','TIFF editering','Status: OK','Profil: GREY;gsuidxx123',[['SE/RA','TIFFedit_MKC']],[['SE/RA','00067990/00000001.TIF']])]):
    version = 'ET090'
    logger.debug('%s Entered AddPremisEvent' % version) # debug info
    
    premis_NS = "{%s}" % SchemaProfile.objects.get(entity='premis_namespace').value 
    xlink_NS = "{%s}" % SchemaProfile.objects.get(entity='xlink_namespace').value
    
    ELs_event = DOC.findall("%sevent" % (premis_NS))

    root = DOC.getroot()

    if len(ELs_event):
        # 1 object
        # Use insert istead of "etree.SubElement" to insert all object's in order
        root.insert(len(ELs_event)+1, etree.Element(premis_NS + "event"))
        ELs_event = DOC.findall("%sevent" % (premis_NS))
        EL_event = ELs_event[len(ELs_event)-1]
    else:
        EL_event = etree.SubElement(root, premis_NS + "event")

    for event in EVENTS:
        # 2.1 eventIdentifier (M, NR)
        EL_eventIdentifier = etree.SubElement(EL_event, premis_NS + "eventIdentifier")
    # 2.1.1 eventIdentifierType (M, NR)
        EL_eventIdentifierType = etree.SubElement(EL_eventIdentifier, premis_NS + "eventIdentifierType").text = event[0]
    # 2.1.2 eventIdentifierValue (M, NR)
        EL_eventIdentifierValue = etree.SubElement(EL_eventIdentifier, premis_NS + "eventIdentifierValue").text = event[1]
    # 2.2 eventType (M, NR)
        EL_eventType = etree.SubElement(EL_event, premis_NS + "eventType").text = event[2]
    # 2.3 eventDateTime (M, NR)
        EL_eventDateTime = etree.SubElement(EL_event, premis_NS + "eventDateTime").text = event[3]
    # 2.4 eventDetail (O, NR)
        if event[4]:
            EL_eventDetail = etree.SubElement(EL_event, premis_NS + "eventDetail").text = event[4]
    # 2.5 eventOutcomeInformation (O, R)
        EL_eventOutcomeInformation = etree.SubElement(EL_event, premis_NS + "eventOutcomeInformation")
    # 2.5.1 eventOutcome (O, NR)
        EL_eventOutcome = etree.SubElement(EL_eventOutcomeInformation, premis_NS + "eventOutcome").text = event[5]
    # 2.5.2 eventOutcomeDetail (O, R)
        EL_eventOutcomeDetail = etree.SubElement(EL_eventOutcomeInformation, premis_NS + "eventOutcomeDetail")
    # 2.5.2.1 eventOutcomeDetailNote (O, NR)
        EL_eventOutcomeDetailNote = etree.SubElement(EL_eventOutcomeDetail, premis_NS + "eventOutcomeDetailNote").text = event[6]
        #* 2.5.2.2 eventOutcomeDetailExtension (O, R)
        for linkingAgentIdentifier in event[7]:
        # 2.6 linkingAgentIdentifier (O, R)
            EL_linkingAgentIdentifier = etree.SubElement(EL_event, premis_NS + "linkingAgentIdentifier")
            # 2.6.1 linkingAgentIdentifierType (M, NR)
            EL_linkingAgentIdentifierType = etree.SubElement(EL_linkingAgentIdentifier, premis_NS + "linkingAgentIdentifierType").text = linkingAgentIdentifier[0]
            # 2.6.2 linkingAgentIdentifierValue (M, NR)
            EL_linkingAgentIdentifierValue = etree.SubElement(EL_linkingAgentIdentifier, premis_NS + "linkingAgentIdentifierValue").text = linkingAgentIdentifier[1]
            #* 2.6.3 linkingAgentRole (O, R)
        for linkingObjectIdentifier in event[8]:
        # 2.7 linkingObjectIdentifier (O, R)
            EL_linkingObjectIdentifier = etree.SubElement(EL_event, premis_NS + "linkingObjectIdentifier")
            # 2.7.1 linkingObjectIdentifierType (M, NR)
            EL_linkingObjectIdentifierType = etree.SubElement(EL_linkingObjectIdentifier, premis_NS + "linkingObjectIdentifierType").text = linkingObjectIdentifier[0]
            # 2.7.2 linkingObjectIdentifierValue (M, NR)
            EL_linkingObjectIdentifierValue = etree.SubElement(EL_linkingObjectIdentifier, premis_NS + "linkingObjectIdentifierValue").text = linkingObjectIdentifier[1]
            #* 2.7.3 linkingObjectRole (O, R)
    return DOC



###############################################
"Get filetree 2"
"""
ET090 - BS130301 - Ready for test
ET091 - BS130324 - Added mimetype application/octet-stream
"""
def GetFiletree2(root,checksumtype=None):
    version = 'ET091'
    logger.debug('%s Entered GetFiletree2' % version) # debug info
    
    try:
        mimefilepath = Path.objects.get(entity='path_mimetypes_definitionfile').value
    except Parameter.DoesNotExist as e:
        if os.path.exists('/ESSArch/config/mime.types'):
            mimefilepath = '/ESSArch/config/mime.types'
        else:
            mimefilepath = '/ESSArch/config/data/mime.types'

    #mimefilepath = Path.objects.get(entity='path_definitions').value + '/'+ Parameter.objects.get(entity='mimetypes_definition').value  # ESSArch Tools
    if os.path.exists(mimefilepath):
        mimetypes.suffix_map={}
        mimetypes.encodings_map={}
        mimetypes.types_map={}
        mimetypes.common_types={}
        mimetypes.init([mimefilepath])
    file_list = []
    exitstatus = 0
    why = None
    try:
        if os.path.exists(root):
            if os.access(root, os.R_OK) and os.access(root, os.W_OK) and os.access(root, os.X_OK):
                for f in os.listdir(root):
                    pathname = os.path.join(root,f)
                    if os.access(pathname, os.R_OK):
                        mode = os.stat(pathname)
                        if stat.S_ISREG(mode[0]):                   # It's a file
                            if checksumtype:
                                f_checksum, errno, why = checksum(pathname, checksumtype)
                                if errno:
                                    return file_list, errno, why
                                f_mimetype = mimetypes.guess_type(pathname,True)[0]
                                if f_mimetype is None:
                                    #if checkmimetypeunknown == 1:
                                    f_mimetype = 'application/octet-stream'
                                    logger.warning('We have an unknown file %s in IP' % f)
                                    #else:
                                    #return file_list, 2, 'Filetype %s is not supported' % f
                            else:
                                f_checksum = None
                                f_mimetype = None
                            file_list.append([utils.str2unicode(f), os.stat(pathname), f_checksum, f_mimetype])
                        elif stat.S_ISDIR(mode[0]):                 # It's a directory
                            dir_file_list, errno, why = GetFiletree2(pathname,checksumtype)
                            if not errno:
                                for df in dir_file_list:
                                    file_list.append([f + '/' + df[0], df[1], df[2], df[3]])
                            else:
                                return file_list, errno, why
                    else:
                        exitstatus = 12
                        why = 'Permision problem for path: %s' % pathname
                        logger.info('GetFiletree2 Permision problem for path: %s' % pathname )
            else:
                exitstatus = 11
                why = 'Permision problem for path: %s' % root
                logger.info('GetFiletree2 Permision problem for path: %s' % root )
        else:
            exitstatus = 13
            why = 'No such file or directory: %s' % root
            logger.info('GetFiletree2 No such file or directory: %s' % root )
    except OSError:
            exitstatus = sys.exc_info()[1][0]
            why = sys.exc_info()[1][1] + ': ' + root
    file_list = sorted(file_list)
    return file_list, exitstatus, why


###############################################
"Return MD5sum for file fname"
"""
ET090 - BS130301 - Ready for test
"""
def checksum(fname,ChecksumAlgorithm = 1):
    version = 'ET090'
    logger.debug('%s Entered checksum' % version) # debug info
    
    #md = []
    #fname = Check().unicode2str(fname)
    #logging.info('Start to create MD5Checksum for: ' + fname)
    #logger.info('Start to create MD5Checksum for: ' + fname)
    if ChecksumAlgorithm == 1:
        m = hashlib.md5()
    elif ChecksumAlgorithm == 2:
        m = hashlib.sha256()
    #chunk = 1048576
    chunk = 1024
    try:
        myfile = open(fname, 'rb')
        data = myfile.read(chunk)
        while data:
            m.update(data)
            data = myfile.read(chunk)
        myfile.close()
    except IOError, why:
        return '',1,str(why)
    else:
        return m.hexdigest(),0,''


###############################################
"Create METS header in METS file"
"""
ET090 - BS130301 - Ready for test
"""
def CreateMetsHdr(agent_list=[],altRecordID_list=[],DocumentID='',TimeZone='Europe/Stockholm',CREATEDATE=None, RECORDSTATUS=None):
    version = 'ET090'
    logger.debug('%s Entered CreateMetsHdr' % version) # debug info
    
    # create mets header
    loc_timezone=pytz.timezone(TimeZone)
    if CREATEDATE is None:
        dt = datetime.datetime.utcnow().replace(microsecond=0,tzinfo=pytz.utc)
        loc_dt_isoformat = dt.astimezone(loc_timezone).isoformat()
    else:
        loc_dt_isoformat = CREATEDATE
    _metsHdr = m.metsHdrType(CREATEDATE=loc_dt_isoformat,RECORDSTATUS=RECORDSTATUS)
    for agent in agent_list:
        _metsHdr.add_agent(m.agentType(ROLE=agent[0], OTHERROLE=agent[1] , TYPE=agent[2], OTHERTYPE=agent[3], name=agent[4], note=agent[5]))
        #_metsHdr.add_agent(m.agentType(ROLE=agent[0], TYPE=agent[1], OTHERTYPE=agent[2], name=agent[3], note=agent[4]))
    for altRecordID in altRecordID_list:
        _metsHdr.add_altRecordID(m.altRecordIDType(TYPE=altRecordID[0],valueOf_=altRecordID[1]))
    _metsHdr.set_metsDocumentID(m.metsDocumentIDType(valueOf_=DocumentID))
    return _metsHdr



###############################################
"Create METS file metadata in METS file"
"""
ET090 - BS130301 - Ready for test
"""
def CreateMetsFileInfo(file_list=[]):
    version = 'ET090'
    logger.debug('%s Entered CreateMetsFileInfo' % version) # debug info
    
    # create amdSec / structMap / fileSec
    _dmdSec = None
    _amdSec = m.amdSecType(ID='amdSec001')
    div_Package = m.divType(LABEL="Package")
    div_ContentDesc = m.divType(LABEL="Content Description", ADMID="amdSec001")
    div_Datafiles = m.divType(LABEL="Datafiles", ADMID="amdSec001")
    div_Package.add_div(div_ContentDesc)
    div_Package.add_div(div_Datafiles)
    _structMap = m.structMapType(div=div_Package)

    _fileSec = m.fileSecType()
    _fileGrp = m.fileGrpType(ID="fgrp001", USE='FILES')
    _fileSec.add_fileGrp(_fileGrp)

    for item in file_list:
        if item[0] == 'fileSec':
            # add entry to fileSec
            _file = m.fileType(
                             ID=item[6],
                             SIZE=item[12],
                             CREATED=item[14],
                             MIMETYPE = item[13],
                             ADMID = item[16],
                             DMDID = item[17],
                             USE = item[15],
                             CHECKSUMTYPE = item[11],
                             CHECKSUM = item[10],
                              )
            _FLocat = m.FLocatType(
                             LOCTYPE=item[7],
                             type_=item[9],
                             href=item[8],
                              )

            _file.set_FLocat(_FLocat)
            _fileGrp.add_file(_file)

            # add entry to structMap
            div_Datafiles.add_fptr(m.fptrType(FILEID=item[6]))

        if item[0] == 'amdSec':
            # add entry to amdSec
            _mdRef = m.mdRefType(ID=item[6], LOCTYPE=item[7],
                                 MDTYPE=item[15], OTHERMDTYPE=item[16], MIMETYPE=item[13],
                                 type_=item[9], href=item[8],
                                 SIZE=item[12], CREATED=item[14],
                                 CHECKSUM=item[10], CHECKSUMTYPE=item[11],
                                )

            _mdSec = m.mdSecType(ID=item[3], mdRef=_mdRef)
            if item[2] == 'techMD':
                _amdSec.add_techMD(_mdSec)
            elif item[2] == 'digiprovMD':
                _amdSec.add_digiprovMD(_mdSec)
    return _dmdSec, _amdSec, _fileSec, _structMap



###############################################
"Validate xml-file"
"""
ET090 - BS130301 - Ready for test
"""
def validate(DOC=None,FILENAME=None,XMLSchema=None):
    version = 'ET090'
    logger.debug('%s Entered validate' % version) # debug info
    
    #XMLSchema = SchemaProfile.objects.get(entity='mets_schemalocation').value
    #if XMLSchema == None:
    #    XMLSchema = SchemaProfile.objects.get(entity='mets_schemalocation').value
    if FILENAME:
        try:
            DOC  =  etree.ElementTree ( file=FILENAME )
        except etree.XMLSyntaxError, detail:
            return 10,str(detail)
        except IOError, detail:
            return 20,str(detail)
    if XMLSchema:
        try:
            root = etree.parse(XMLSchema)
        except etree.XMLSyntaxError, detail:
            return 11,str(detail)
        except IOError, detail:
            return 21,str(detail)
    else:
        # Create validation schema
        xsd_NS = "{%s}" % SchemaProfile.objects.get(entity='xsd_namespace').value
        NSMAP = {'xsd' : SchemaProfile.objects.get(entity='xsd_namespace').value}
        root = etree.Element(xsd_NS + "schema", nsmap=NSMAP) # lxml only!
        root.attrib["elementFormDefault"] = "qualified"
        RootEL_schema = etree.ElementTree(element=root, file=None)
        SchemaLocations,errno,why = getSchemaLocation(DOC)
        for SCHEMALOCATION in SchemaLocations:
            etree.SubElement(root, xsd_NS + "import", attrib={"namespace" : SCHEMALOCATION[0],
                                                              "schemaLocation" : SCHEMALOCATION[1]})
        #print etree.tostring(RootEL_schema,encoding='UTF-8', xml_declaration=True, pretty_print=True)
    try:
        xmlschema = etree.XMLSchema(root)
    except etree.XMLSchemaParseError, details:

        ################# Debug start #######################
        # Write XMLSchema to debugfile
        #debugfile = '/ESSArch/log/debug/XMLSchema_1_%s.xsd' % datetime.datetime.now().isoformat()
        debugfile = '/ESSArch/log/debug/XMLSchema_1_%s.xsd' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
        errno_ignore,why_ignore = writeToFile(RootEL_schema,debugfile)
        # Write XMLdoc to debugfile
        #debugfile = '/ESSArch/log/debug/XML_DOC_1_%s.xml' % datetime.datetime.now().isoformat()
        debugfile = '/ESSArch/log/debug/XML_DOC_1_%s.xml' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
        errno_ignore,why_ignore = writeToFile(DOC,debugfile)
        # Write getSchemaLocation to debugfile
        #debugfile = '/ESSArch/log/debug/getSchemaLocation_1_%s.log' % datetime.datetime.now().isoformat()
        debugfile = '/ESSArch/log/debug/getSchemaLocation_1_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
        debugfile_object = open(debugfile, 'w')
        debugfile_object.write(str(SchemaLocations))
        debugfile_object.close()
        # Write ParseError_details to debugfile
        #debugfile = '/ESSArch/log/debug/ParseError_details_1_%s.log' % datetime.datetime.now().isoformat()
        debugfile = '/ESSArch/log/debug/ParseError_details_1_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
        debugfile_object = open(debugfile, 'w')
        debugfile_object.write(str(details))
        debugfile_object.close()
        ################# Debug end #######################
        time.sleep(60)
        try:
            xmlschema = etree.XMLSchema(root)
        except etree.XMLSchemaParseError, details:

            ################# Debug start #######################
            # Write XMLSchema to debugfile
            #debugfile = '/ESSArch/log/debug/XMLSchema_2_%s.xsd' % datetime.datetime.now().isoformat()
            debugfile = '/ESSArch/log/debug/XMLSchema_2_%s.xsd' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
            errno_ignore,why_ignore = writeToFile(RootEL_schema,debugfile)
            # Write XMLdoc to debugfile
            #debugfile = '/ESSArch/log/debug/XML_DOC_2_%s.xml' % datetime.datetime.now().isoformat()
            debugfile = '/ESSArch/log/debug/XML_DOC_2_%s.xml' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
            errno_ignore,why_ignore = writeToFile(DOC,debugfile)
            # Write getSchemaLocation to debugfile
            #debugfile = '/ESSArch/log/debug/getSchemaLocation_2_%s.log' % datetime.datetime.now().isoformat()
            debugfile = '/ESSArch/log/debug/getSchemaLocation_2_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
            debugfile_object = open(debugfile, 'w')
            debugfile_object.write(str(SchemaLocations))
            debugfile_object.close()
            # Write ParseError_details to debugfile
            #debugfile = '/ESSArch/log/debug/ParseError_details_2_%s.log' % datetime.datetime.now().isoformat()
            debugfile = '/ESSArch/log/debug/ParseError_details_2_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
            debugfile_object = open(debugfile, 'w')
            debugfile_object.write(str(details))
            debugfile_object.close()
            ################# Debug end #######################
            time.sleep(300)
            try:
                xmlschema = etree.XMLSchema(root)
            except etree.XMLSchemaParseError, details:

                ################# Debug start #######################
                # Write XMLSchema to debugfile
                #debugfile = '/ESSArch/log/debug/XMLSchema_3_%s.xsd' % datetime.datetime.now().isoformat()
                debugfile = '/ESSArch/log/debug/XMLSchema_3_%s.xsd' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
                errno_ignore,why_ignore = writeToFile(RootEL_schema,debugfile)
                # Write XMLdoc to debugfile
                #debugfile = '/ESSArch/log/debug/XML_DOC_3_%s.xml' % datetime.datetime.now().isoformat()
                debugfile = '/ESSArch/log/debug/XML_DOC_3_%s.xml' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
                errno_ignore,why_ignore = writeToFile(DOC,debugfile)
                # Write getSchemaLocation to debugfile
                #debugfile = '/ESSArch/log/debug/getSchemaLocation_3_%s.log' % datetime.datetime.now().isoformat()
                debugfile = '/ESSArch/log/debug/getSchemaLocation_3_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
                debugfile_object = open(debugfile, 'w')
                debugfile_object.write(str(SchemaLocations))
                debugfile_object.close()
                # Write ParseError_details to debugfile
                #debugfile = '/ESSArch/log/debug/ParseError_details_3_%s.log' % datetime.datetime.now().isoformat()
                debugfile = '/ESSArch/log/debug/ParseError_details_3_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
                debugfile_object = open(debugfile, 'w')
                debugfile_object.write(str(details))
                debugfile_object.close()
                ################# Debug end #######################
                return 30,str(details)
        #return 30,str(details)
    if not xmlschema.validate(DOC):
        # Convert xmlschema.error_log to python list
        error_log = [['column','domain','domain_name','filename','level','level_name','line','message','type','type_name']]
        for LogEntry in xmlschema.error_log:
            error_log.append([LogEntry.column,LogEntry.domain,LogEntry.domain_name,LogEntry.filename,LogEntry.level,LogEntry.level_name,LogEntry.line,unicode(LogEntry.
message.encode('iso-8859-1'), 'iso-8859-1'),LogEntry.type,LogEntry.type_name])

        ################# Debug start #######################
        # Write xmlshcme.error_log to debugfile
        #debugfile = '/ESSArch/log/debug/validate_error_log_%s.log' % datetime.datetime.now().isoformat()
        debugfile = '/ESSArch/log/debug/validate_error_log_%s.log' % datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S.%f")
        debugfile_object = open(debugfile, 'w')
        for log_entry in error_log:
            debugfile_object.write(str(log_entry)+'\n')
        debugfile_object.close()
        ################# Debug end #######################

        #print str(error_log)
        return 1,str(error_log)
    return 0,'OK'



###############################################
"Get Schems location"
"""
ET090 - BS130301 - Ready for test
"""
def getSchemaLocation(DOC=None,FILENAME=None,NS='http://xml.ra.se/PREMIS',PREFIX='premis'):
    version = 'ET090'
    logger.debug('%s Entered getSchemaLocation' % version) # debug info
    
    if FILENAME:
        try:
            DOC  =  etree.ElementTree ( file=FILENAME )
        except etree.XMLSyntaxError, detail:
            return [['','']],10,str(detail)
        except IOError, detail:
            return [['','']],20,str(detail)
    res=[]

    EL_root = DOC.getroot()
    
    xlink_NS = "{%s}" % EL_root.nsmap['xlink']
    xsi_NS = "{%s}" % EL_root.nsmap['xsi']
    all_schemaLocations = DOC.findall("[@%sschemaLocation]" % xsi_NS)
    for schemaLocation in all_schemaLocations:
        a = 0
        for item in schemaLocation.attrib["%sschemaLocation" % xsi_NS].split():
            if a == 0:
                ns_item = item
                a = 1
            elif a == 1: 
                res.append([ns_item,item])
                a = 0
    all_schemaLocations = DOC.findall(".//*[@%sschemaLocation]" % xsi_NS)
    for schemaLocation in all_schemaLocations:
        a = 0
        for item in schemaLocation.attrib["%sschemaLocation" % xsi_NS].split():
            if a == 0:
                ns_item = item
                a = 1
            elif a == 1:
                res.append([ns_item,item])
                a = 0
    return res,0,''



###############################################
"Write to XML file"
"""
ET090 - BS130301 - Ready for test
"""
def writeToFile(DOC=None,FILENAME=None):
    version = 'ET090'
    logger.debug('%s Entered writeToFile' % version) # debug info
    
    try:
        DOC.write(FILENAME,encoding='UTF-8',xml_declaration=True,pretty_print=True)
    except etree.XMLSyntaxError, detail:
        return 10,str(detail)
    except IOError, detail:
        return 20,str(detail)
    else:
        return 0,'OK'

###############################################
"Check if file is locked"
"""
ET091 - BS130324 - Ready for test
"""
class FileLock(object):

    def __init__(self, fname, timeout=None):
        self.fname = fname
        self.timeout = timeout

    def is_locked(self):
        version = 'ET091'
        logger.debug('%s Entered FileLock' % version) # debug info
        # We aren't locked
        if not self.valid_lock():
            return False

        # We are locked
        if not self.timeout:
            return True

        # Locked, but want to wait for an unlock
        interval = .1
        intervals = int(self.timeout / interval)

        while intervals:
            if self.valid_lock():
                intervals -= 1
                time.sleep(interval)
                print('stopping %s' % intervals)        
            else:
                return False

        # check one last time
        if self.valid_lock():
            # still locked :(
            return True
        else:
            return False

    def valid_lock(self):
        """Checks if a file is locked by opening it in append mode.
        If no exception thrown, then the file is not locked.
        """
        locked = None
        file_object = None
        if os.path.exists(self.fname):
            try:
                buffer_size = 8
                # Opening file in append mode and read the first 8 characters.
                file_object = open(self.fname, 'a', buffer_size)
                if file_object:
                    locked = False 
            except IOError, message:
                locked = True
            finally:
                if file_object:
                    file_object.close()
        else:
            locked = None
        return locked

