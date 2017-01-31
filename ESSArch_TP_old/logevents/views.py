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
from django.template import Context, loader, RequestContext 
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.http import urlquote
from django.shortcuts import render_to_response, get_object_or_404, render
#from django.core.context_processors import csrf
from django.middleware import csrf
from django.contrib.auth.decorators import login_required
import os, uuid, operator

# import the logging library and get an instance of a logger
import logging
logger = logging.getLogger('code.exceptions')

# own models etc
from ip.models import InformationPackage
#from configuration.models import Parameter, LogEvent, Path, ControlAreaForm_file 
from configuration.models import Parameter, LogEvent, Path 
from newlogeventform import NewLogEventForm, NewLogFileForm
import lib.utils as lu
import lib.app_tools as lat

from esscore.rest.uploadchunkedrestclient import UploadChunkedRestClient, UploadChunkedRestException
import requests
import  requests.packages
from urlparse import urljoin
import jsonpickle



@login_required
def index(request):
    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()    
    t = loader.get_template('logevents/index.html')
    c = RequestContext(request)
    c['zone'] = zone
    return HttpResponse(t.render(c))
    

"List all logfiles at logfiles path"
###############################################
@login_required
def listlog(request):
    #ip = get_object_or_404(InformationPackage, pk=id)

    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()    
    
    # get a list of IPs from db
    ips = InformationPackage.objects.all()

    # need to find out path to log files
    logfilepath = lat.getLogFilePath()
    #print logfilepath
    # if zone3 add user home directories to path etccontrolarea/create.html
    if zone == 'zone3' :
        logfilepath = logfilepath +'/'+ str(request.user)
        
    # need to search through all log files to find the one that we want
    templatefile_log = Parameter.objects.get(entity="ip_logfile").value
    loglist = lat.getLogFiles(logfilepath, templatefile_log)
    #print templatefile_log
    #print logfilepath
    # reverse order so that the latest logs come first
    loglist = sorted(loglist, key=operator.itemgetter("createdate"))
    #for i in loglist:
    #    print i
    
    # look for mismatch db and filesystem
    found = 0 # not found any matching IP
    for log in loglist:
        for ip in ips:
            if ip.uuid == log["uuid"] :
                log[ "state" ] = ip.state
                found = 1  # found one match
        if not found :
            if  zone == 'zone3':
                log[ "state" ] = 'Processing'
            else:
                log[ "state" ] = 'Stale'
        found = 0 # reset flag
        
        # generate link URL
        log[ "link" ] = "%s/%s/%s/%s/%s" % ( log["uuid"], 
                                                log["archivist_organization"], 
                                                log["label"], 
                                                #log["startdate"],
                                                #log["enddate"], 
                                                log["iptype"], 
                                                log["createdate"] )
                                          
    c = {'log_list':loglist,
         'zone':zone,
         #'ip':ip,
         }
    return render_to_response('logevents/list.html', c,
                              context_instance=RequestContext(request) )


"View and add logevents to logfile"
###############################################controlarea/create.html
@login_required
def viewlog(request, uuid, archivist_organization, label, iptype, createdate):
#def viewlog(request, uuid, archivist_organization, label, startdate, enddate, iptype, createdate):
#def viewlog(request):
    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()    
    
    # need to find out path to log files
    logfilepath = lat.getLogFilePath()
    
    # if zone3 add user home directories to path etc
    if zone == 'zone3' :
        logfilepath = logfilepath +'/'+ str(request.user)
    
    # need to search through all log files to find the one that we want
    templatefile_log = Parameter.objects.get(entity="ip_logfile").value
    loglist = lat.getLogFiles(logfilepath, templatefile_log )
    logfile = None
    for log in loglist:
        #print log
        if log["uuid"] == uuid :
            logfile = log[ "fullpath" ]

    if logfile != None and logfile != "":

        if request.method == 'POST': # If the form has been submitted...
            form = NewLogEventForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                
                # get clean context data
                contextdata = form.cleaned_data
            
                # check status of event
                t =  contextdata["eventOutcome"]
                status = 0
                if t!="Ok":
                    status = 1
                
                # fetch logged in user
                user = str(request.user)

                # add event to logfile                                                               
                lat.appendToLogFile( logfile,
                         #form.cleaned_data[ "eventType" ],
                         contextdata[ "eventType" ],
                         status,
                         #form.cleaned_data[ "eventOutcomeDetailNote" ],
                         contextdata[ "eventOutcomeDetailNote" ],
                         user,
                         uuid )

                # get eventDetail for log
                eventDetail=LogEvent.objects.filter( eventType=contextdata["eventType"])[0].eventDetail
                logger.info('Successfully appended event "%s" to package IP %s', eventDetail, label)

            else:
                logger.error('Form NewLogEventForm is not valid.')
                #print form.data, form.errors

        #else:
        form = NewLogEventForm()

        # we have the log file, need to generate the report.
        content = lat.getLogEvents( logfile )
        
        # reverse order so that the latest logs come first
        content.reverse()
        
        #link = urlquote( "%s/%s/%s/%s/%s/%s/%s" % ( uuid, creator, label, startdate, enddate, iptype, createdate ) )
        #link = urlquote( "%s/%s/%s/%s/%s/%s/%s" % ( uuid, archivist_organization, label, startdate, enddate, iptype, createdate ) )
        link = urlquote( "%s/%s/%s/%s/%s" % ( uuid, archivist_organization, label, iptype, createdate ) )
        c = { 'log_content':content, 
              'form': form,
              'link': link,
              'uuid': uuid,
              'zone':zone,
              'archivist_organization': archivist_organization,
              'label':label, 
              }
        #c.update(csrf(request))
        #return render_to_response( 'logevents/view.html', c, context_instance=RequestContext(request) )
        return render( request, 'logevents/view.html', c )

    else:
        # something went wrong and we have a problem.
        raise Http404


"Create log circular eq logfile"
###############################################
@login_required
def createlog(request):

    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()    

    # get a list of IPs from db
    ips = InformationPackage.objects.all()

    # need to search through all spec files to present them
    file_path = Path.objects.get(entity="path_ingest_reception").value
    spec_file = Parameter.objects.get(entity="package_descriptionfile").value
    file_list = lat.getFiles(file_path, spec_file )
    
    # look for mismatch db and filesystem
    found = 0 # not found any matching IP
    for fil in file_list:
        if fil["ip_uuid"][:5] == 'UUID:' or fil["ip_uuid"][:5] == 'RAID:' : 
            ip_uuid = fil["ip_uuid"][5:]
        else :
            ip_uuid = fil["ip_uuid"]
        for ip in ips:
            if ip.uuid == ip_uuid :
                fil[ "state" ] = ip.state
                found = 1  # found one match
        if not found :
            if  zone == 'zone3':
                fil[ "state" ] = 'Processing'
            else:
                fil[ "state" ] = 'Not received'
        found = 0 # reset flag
    
#    # declare files as delivered to us
#    for i in file_list:
#        i['state']='Delivered' 
#        print i
    
    if request.method == 'POST': # If the form has been submitted...
        form = NewLogFileForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            try: 
                #opt = [] 
                opt = request.POST.getlist('checkbox')
                #print opt 
            except:
                pass
            
            # get clean context data
            contextdata = form.cleaned_data
            #spec_file = contextdata["sourceroot"]
            
            # agent e.q user
            agent = str(request.user)
            
            for filename in opt:
                print filename
                contextdata["filename"] = filename
                contextdata["iplocation"] = os.path.split(filename)[0]
                print contextdata
                
                # prepare IP
                ip, errno, why = lat.prepareIP(agent, contextdata)
                if errno: 
                    logger.error(why)
                    c = { 'message': why }
                    c.update(csrf(request))
		    logger.error('Could not prepare package IP %s and create log file at gate %s' % (ip.label,ip.directory))
                    return render_to_response('status.html', c, context_instance=RequestContext(request) )
                else:
                    logger.info('Successfully prepared package IP %s and created log file at gate' % ip.label)

            # exit form
            return HttpResponseRedirect( '/logevents/list' )
        
        else:
            logger.error('Form PrepareFormSE/NO is not valid.')
            #print form.data, form.errors
            c = {'form': form,
                 'zone':zone,
                 }
            c.update(csrf(request))
            return render_to_response( 'logevents/create.html', c, context_instance=RequestContext(request) )
            #return render_to_response( 'logevents/list.html', c, context_instance=RequestContext(request) )
                    
    else:
        form = NewLogFileForm() # A unbound form
        #form = NewLogFileForm
        #print i['ip_uuid']
        #print k[0]
        #print k['id']
        #form_class.FileSelect_CHOICES = k
        #form = form_class()  
        #print form.errors
        #print form.data
        c = {'form':form,
             'zone':zone,
             'file_list':file_list,
             }
        c.update(csrf(request))
        return render_to_response('logevents/create.html', c, context_instance=RequestContext(request) )

            
def _initialize_requests_session(ruser, rpass, cert_verify=True, disable_warnings=False):
    if disable_warnings == True:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests_session = requests.Session()
    requests_session.verify = cert_verify
    requests_session.auth = (ruser, rpass)
    return requests_session
