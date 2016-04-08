from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from ip.models import InformationPackage
from configuration.models import (
                                  Path,
                                  Parameter,
                                  )

from .forms import (
                    SubmitForm,
                    SubmitFormWithoutEmail,
                    )

from esscore.rest.uploadchunkedrestclient import UploadChunkedRestClient, UploadChunkedRestException

from urlparse import urljoin

import lib.app_tools as lat
import shutil
import requests
import  requests.packages
import os
import logging
logger = logging.getLogger('code.exceptions')

class SubmitIPList(View):
    template_name = 'submit/list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = RequestContext(request)
        context['label'] = 'Select which information package to submit'

        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()    
    
        # get a list of IPs from db
        objs = InformationPackage.objects.filter(state='Created')
        
        context['informationpackages'] = objs
        context['zone'] = zone      
        return render(request, self.template_name, context)

class SubmitIPCreate(View):
    template_name = 'submit/create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Submit information packages'

        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()   
        
        #id = request.GET.get('id',None) 
    
        id = self.kwargs['id']
        # get IP from db
        ip = get_object_or_404(InformationPackage, pk=id)
        destination = Path.objects.get(entity="path_ingest_reception").value
        remote_server_string = Parameter.objects.get(entity='preservation_organization_receiver').value
        remote_server = remote_server_string.split(',')
        if len(remote_server) == 3:
            remote_flag = True
        else:
            remote_flag = False

        if remote_flag:
            # init uploadclient
            base_url, ruser, rpass = remote_server
            preservation_organization_receiver = '- Remote server: %s' % base_url
        else:
            preservation_organization_receiver = '- Local filesystem: %s' % destination
        
        email_to = Parameter.objects.get(entity='preservation_email_receiver').value
        sendemail_flag = email_to.__contains__('@')

        initialvalues = {}
        initialvalues['preservation_organization_receiver'] = preservation_organization_receiver
        initialvalues['email_from'] = str(request.user.email) # logged in user
        initialvalues['email_to'] = email_to # default email receiver
        initialvalues['destination'] = destination
        if sendemail_flag:
            form = SubmitForm( initial=initialvalues )
        else:
            form = SubmitFormWithoutEmail( initial=initialvalues )
        
        context['form'] = form
        context['zone'] = zone
        context['ip'] = ip
        context['sourceroot'] = ip.directory
        context['sendemail'] = sendemail_flag
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Submit information packages'
        
        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()    
        
        id = self.kwargs['id']
        #id = request.POST.get('id',None) 
        
        # get IP from db
        ip = get_object_or_404(InformationPackage, pk=id)
        
        destination = Path.objects.get(entity="path_ingest_reception").value

        email_to = Parameter.objects.get(entity='preservation_email_receiver').value
        sendemail_flag = email_to.__contains__('@')
        
        if sendemail_flag:
            form = SubmitForm(request.POST) # A form bound to the POST data
        else:
            form = SubmitFormWithoutEmail(request.POST)
            
        if form.is_valid(): # All validation rules pass
            
            # which package description file and compressed IP file
            f_name = ip.directory + '/' + Parameter.objects.get(entity="package_descriptionfile").value
            ip_fname = ip.directory + '/' + ip.uuid+'.tar'
            
            # get clean context data from form
            contextdata = form.cleaned_data
                        
            # move ip from source to destination
            dir_src = ip.directory

            remote_server_string = Parameter.objects.get(entity='preservation_organization_receiver').value
            remote_server = remote_server_string.split(',')
            if len(remote_server) == 3:
                remote_flag = True
            else:
                remote_flag = False

            if remote_flag:
                # init uploadclient
                base_url, ruser, rpass = remote_server
                upload_rest_endpoint = urljoin(base_url, '/api/create_reception_upload')        
                requests_session =  _initialize_requests_session(ruser, rpass, cert_verify=False, disable_warnings=True)           
                uploadclient = UploadChunkedRestClient(requests_session, upload_rest_endpoint)
            else:
                # Create a new information package folder ready for deliver
                i = 1
                while os.path.exists( os.path.join( destination, "ip%d"%i ) ):
                    i+=1
                delivery_root = os.path.join( destination, "ip%d"%i )
                os.makedirs( delivery_root )          
                dir_dst = delivery_root+'/'      
            
            for filename in os.listdir(dir_src):
                
                src_file = os.path.join(dir_src, filename)
                if remote_flag:
                    uploadclient.upload(src_file, ip.uuid)
                else:
                    dst_file = os.path.join(dir_dst, filename)
                    #shutil.move(src_file, dst_file)
                    shutil.copy(src_file, dst_file)
            logger.info('Successfully delivered package IP %s to destination', ip.label )
            
            # remove source directory
            #shutil.rmtree(ip.directory)

            # mark IP as delivered
            ip.state = "Submitted"
            #if not remote_flag:
            #    ip.directory = delivery_root 
            ip.progress = 100
            ip.save()

            if sendemail_flag:
                # email parameters
                email_subject = contextdata['email_subject']
                email_body = contextdata['email_body']
                email_to = contextdata['email_to'] 
                email_from = str(request.user.email) # logged in user
    
                logger.info('send_mail of package description %s starts' % f_name)
                
                # create and send email with attached package description file            
                msg = EmailMessage(email_subject, email_body, email_from, [email_to])
                msg.attach_file(f_name, 'application/xml')
                msg.send(fail_silently=False)
                
                logger.info('send_mail of package description %s ends' % f_name)
        
            return HttpResponseRedirect( '/submit/submitiplist/' )
        else:
            logger.error('Form DeliverForm is not valid.')
            #print form.data, form.errors
            email_to = Parameter.objects.get(entity='preservation_email_receiver').value
            sendemail_flag = email_to.__contains__('@')
            context['form'] = form
            context['zone'] = zone
            context['ip'] = ip
            context['sourceroot'] = ip.directory
            context['sendemail'] = sendemail_flag
            return render(request, self.template_name, context)

def _initialize_requests_session(ruser, rpass, cert_verify=True, disable_warnings=False):
    if disable_warnings == True:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests_session = requests.Session()
    requests_session.verify = cert_verify
    requests_session.auth = (ruser, rpass)
    return requests_session