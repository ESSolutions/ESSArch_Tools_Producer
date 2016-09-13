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
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
#from django.core.context_processors import csrf
from django.middleware import csrf
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils.http import urlquote
import os, os.path, uuid, datetime, forms, pytz, shutil, time, operator, pdb
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
#file upload
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
# import the logging library and get an instance of a logger
import logging
logger = logging.getLogger('code.exceptions')

import re
import shutil
import json

from django.views.generic import View
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from chunked_upload.settings import MAX_BYTES
#from chunked_upload.views import ChunkedUploadBaseView
from chunked_upload.models import ChunkedUpload
from chunked_upload.response import Response
from chunked_upload.constants import http_status, COMPLETE
from chunked_upload.exceptions import ChunkedUploadError

from config.settings import MEDIA_ROOT
from models import ETPupload

# from ESSArch Tools
from ip.models import InformationPackage
from configuration.models import Parameter, LogEvent, SchemaProfile, IPParameter, Path
from .forms import PrepareFormSE, PrepareFormNO, PrepareFormEC, CreateFormSE, CreateFormNO, CreateFormEC
import lib.utils as lu
import lib.app_tools as lat

'''
@login_required
def index(request):
    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()    
    t = loader.get_template('create/index.html')
    c = RequestContext(request)
    c['zone'] = zone
    return HttpResponse(t.render(c))
'''

class PrepareIPCreate(View):
    #template_name = 'create/prepare_create.html'
    template_name = 'create/prepare_create_new.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Prepare new information packages'

        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()   

        # Present only prepared IPs 
        ip = InformationPackage.objects.filter(state='Prepared')

        initialvalues = {}
        initialvalues['destinationroot'] = lat.getLogFilePath()
        if site_profile == "SE":
            form = PrepareFormSE(initial=initialvalues) # Form with defaults
        if site_profile == "NO":
            #form = PrepareFormNO(initial=initialvalues) # Form with defaults
            form = PrepareFormEC(initial=initialvalues) # Form with defaults
        
        context['form'] = form
        context['zone'] = zone
        context['informationpackages'] = ip
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Submit information packages'
        
        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()

        if site_profile == "SE":
            form = PrepareFormSE(request.POST) # A form bound to the POST data
        if site_profile == "NO":
            #form = PrepareFormNO(request.POST) # A form bound to the POST data
            form = PrepareFormEC(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            
            # get clean context data
            contextdata = form.cleaned_data
            
            # agent e.q user
            agent = str(request.user)

            # prepare IP
            ip,errno,why = lat.prepareIP(agent, contextdata)
            if errno: 
                logger.error(why)
                c = { 'message': why }
                c.update(csrf(request))
                return render_to_response('status.html', c, context_instance=RequestContext(request) )
            else:
                logger.info('Successfully prepared package IP %s and created log file', ip.label)

            # exit form
            return HttpResponseRedirect( '/create/createiplist' )
            
        else:
            logger.error('Form PrepareFormSE/NO is not valid.')
            #print form.data, form.errors
            context['form'] = form
            context['zone'] = zone
            return render(request, self.template_name, context)

class CreateIPList(View):
    template_name = 'create/list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Select which information package to create'

        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()   

        # Present only prepared IPs 
        ip = InformationPackage.objects.filter(state='Prepared')

        context['zone'] = zone
        context['informationpackages'] = ip
        return render(request, self.template_name, context)

class CreateIP(View):
    template_name = 'create/create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Create information package'

        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()    
    
        id = self.kwargs['id']
    
        # get IP from db
        ip = get_object_or_404(InformationPackage, pk=id)
    
        destination_path = Path.objects.get(entity="path_ingest_reception").value

        initialvalues = IPParameter.objects.all().values()[0]
        initialvalues['destinationroot'] = destination_path
        initialvalues['archivist_organization'] = ip.archivist_organization
        initialvalues['label'] = ip.label
        initialvalues['type'] = ip.iptype
        if site_profile == "SE":
            form = CreateFormSE( initial=initialvalues )
        if site_profile == "NO":
            #form = CreateFormNO( initial=initialvalues )
            form = CreateFormEC( initial=initialvalues )

        #context['label'] = 'Create information package ' + ip.label ' from ' + ip.archivist_organization 
        context['form'] = form
        context['zone'] = zone
        context['ip'] = ip
        context['destinationroot'] = destination_path
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Submit information packages'
        
        # Get current site_profile and zone
        site_profile, zone = lat.getSiteZone()    
        
        id = self.kwargs['id']
        
        # get IP from db
        ip = get_object_or_404(InformationPackage, pk=id)

        if site_profile == "SE":
            form = CreateFormSE(request.POST) # A form bound to the POST data
        if site_profile == "NO":
            #form = CreateFormNO(request.POST) # A form bound to the POST data
            form = CreateFormEC(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            
            # get clean context data from form
            contextdata = form.cleaned_data

            # create IP, if unsuccessful show status
            ip, errno, why = lat.createIP(ip, contextdata)
            if errno: 
                logger.error('Could not create IP: %s', why)
                c = { 'message': why }
                c.update(csrf(request))
                return render_to_response('status.html', c, context_instance=RequestContext(request) )
            else:
                logger.info('Successfully created package IP %s', ip.label)

            # exit form
            return HttpResponseRedirect('/create/createiplist')

        else:
            logger.error('Form CreateFormSE/NO is not valid.')
            #print form.data, form.errors
            context['form'] = form
            context['zone'] = zone
            context['ip'] = ip
            return render(request, self.template_name, context)

'''
"View IPs and prepare new IPs"
###############################################
@login_required
#def viewIPs(request, uuid, creator, label, iptype, createdate):
def viewIPs(request):    
    
    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()
        
    # Prepare IPs
    if request.method == 'POST': # If the form has been submitted...
        if site_profile == "SE":
            form = PrepareFormSE(request.POST) # A form bound to the POST data
        if site_profile == "NO":
            form = PrepareFormNO(request.POST) # A form bound to the POST data
        #form = PrepareForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            # get clean context data
            contextdata = form.cleaned_data
            
            # agent e.q user
            agent = str(request.user)

            # prepare IP
            ip,errno,why = lat.prepareIP(agent, contextdata)
            if errno: 
                logger.error(why)
                c = { 'message': why }
                c.update(csrf(request))
                return render_to_response('status.html', c, context_instance=RequestContext(request) )
            else:
                logger.info('Successfully prepared package IP %s and created log file', ip.label)

            # exit form
            return HttpResponseRedirect( '/create/view' )
            
        else:
            logger.error('Form PrepareFormSE/NO is not valid.')
            #print form.data, form.errors
            c = {'form': form,
                 'zone':zone,
                 }
            c.update(csrf(request))
            return render_to_response( 'create/view.html', c, context_instance=RequestContext(request) )
    
    else:
        initialvalues = {'destinationroot':lat.getLogFilePath()}
        if site_profile == "SE":
            form = PrepareFormSE(initial=initialvalues) # Form with defaults
        if site_profile == "NO":
            form = PrepareFormNO(initial=initialvalues) # Form with defaults
        #form = PrepareForm(initial=initialvalues) # Form with defaults

    # Present only prepared IPs 
    ip = InformationPackage.objects.filter(state='Prepared')

    c = {'form': form,
         'zone':zone, 
         'informationpackages': ip,
        #'link': link,
         }
    c.update(csrf(request))
    return render_to_response( 'create/view.html', c, context_instance=RequestContext(request) )

"Create IPs"
###############################################
#@permission_required('ip.Can_view_ip_menu')
@login_required
def createip(request, id):
    ip = get_object_or_404(InformationPackage, pk=id)


    # Get current site_profile and zone
    site_profile, zone = lat.getSiteZone()

    # need to find out path for destination
    destination_path = Path.objects.get(entity="path_preingest_reception").value
    
    if request.method == 'POST': # If the form has been submitted...
        if site_profile == "SE":
            form = forms.CreateFormSE(request.POST) # A form bound to the POST data
        if site_profile == "NO":
            form = forms.CreateFormNO(request.POST) # A form bound to the POST data
        #form = forms.CreateForm(request.POST) # A form bound to the POST data
        #pdb.set_trace()
        if form.is_valid(): # All validation rules pass
            
            # get clean context data from form
            contextdata = form.cleaned_data

            # create IP, if unsuccessful show status
            ip, errno, why = lat.createIP(ip, contextdata)
            if errno: 
                logger.error('Could not create IP: %s', why)
                c = { 'message': why }
                c.update(csrf(request))
                return render_to_response('status.html', c, context_instance=RequestContext(request) )
            else:
                logger.info('Successfully created package IP %s', ip.label)

            # exit form
            return HttpResponseRedirect( '/create/view' )

        else:
            logger.error('Form CreateFormSE/NO is not valid.')
            #print form.data, form.errors
            c = {'form': form,
                 'zone':zone,
                 'ip':ip,
                }
            c.update(csrf(request))
            return render_to_response('create/create.html', c, context_instance=RequestContext(request) )
    else:
        initialvalues = IPParameter.objects.all().values()[0]
        initialvalues['destinationroot'] = destination_path
        initialvalues['archivist_organization'] = ip.archivist_organization
        initialvalues['label'] = ip.label
        #initialvalues['startdate'] = ip.startdate
        #initialvalues['enddate'] = ip.enddate
        initialvalues['type'] = ip.iptype
        if site_profile == "SE":
            form = forms.CreateFormSE( initial=initialvalues )
        if site_profile == "NO":
            form = forms.CreateFormNO( initial=initialvalues )
        #form = forms.CreateForm( initial=initialvalues )
        
    c = {'form':form,
         'zone':zone,
         'ip':ip,
         'destinationroot':destination_path,
         }
    c.update(csrf(request))
    return render_to_response('create/create.html', c, context_instance=RequestContext(request) )
'''

class IPcontentasJSON(View):

    def dispatch(self, *args, **kwargs):
    
        return super(IPcontentasJSON, self).dispatch( *args, **kwargs)
        
    def getDirectoryInfo(self, *args, **kwargs):

        ipid = self.kwargs['ipid']
        thisip = get_object_or_404(InformationPackage, pk=ipid)
        #print 'thisip directory'
        #print thisip.directory
        contentpath = thisip.directory + '/' + thisip.uuid + '/content/'
        listofcontent = os.listdir(contentpath)
        listofcontent.sort()
        #print 'listofcontent'
        #print listofcontent
        #print listofcontent[0]

        return listofcontent

    def json_response(self, request):
        
        data = self.getDirectoryInfo()
        return HttpResponse(
            #data
            json.dumps(data, cls=DjangoJSONEncoder)
        )
    def get(self, request, *args, **kwargs):
        
        return self.json_response(request)


class ChunkedUploadBaseView(View):
    """
    Base view for the rest of chunked upload views.
    """

    # Has to be a ChunkedUpload subclass
    model = ChunkedUpload

    def get_queryset(self, request):
        """
        Get (and filter) ChunkedUpload queryset.
        By default, users can only continue uploading their own uploads.
        """
        queryset = self.model.objects.all()
        if hasattr(request, 'user') and request.user.is_authenticated():
            queryset = queryset.filter(user=request.user)
        return queryset

    def validate(self, request):
        """
        Placeholder method to define extra validation.
        Must raise ChunkedUploadError if validation fails.
        """

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        Called *only* if POST is successful.
        """
        return {}

    def pre_save(self, chunked_upload, request, new=False):
        """
        Placeholder method for calling before saving an object.
        May be used to set attributes on the object that are implicit
        in either the request, or the url.
        """

    def save(self, chunked_upload, request, new=False):
        """
        Method that calls save(). Overriding may be useful is save() needs
        special args or kwargs.
        """
        chunked_upload.save()

    def post_save(self, chunked_upload, request, new=False):
        """
        Placeholder method for calling after saving an object.
        """

    def _save(self, chunked_upload):
        """
        Wraps save() method.
        """
        new = chunked_upload.id is None
        self.pre_save(chunked_upload, self.request, new=new)
        self.save(chunked_upload, self.request, new=new)
        self.post_save(chunked_upload, self.request, new=new)

    def check_permissions(self, request):
        """
        Grants permission to start/continue an upload based on the request.
        """
        if hasattr(request, 'user') and not request.user.is_authenticated():
            raise ChunkedUploadError(
                status=http_status.HTTP_403_FORBIDDEN,
                detail='Authentication credentials were not provided'
            )

    def _post(self, request, *args, **kwargs):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        try:
            self.check_permissions(request)
            return self._post(request, *args, **kwargs)
        except ChunkedUploadError as error:
            return Response(error.data, status=error.status_code)

class ChunkedUploadView(ChunkedUploadBaseView):
    """
    Uploads large files in multiple chunks. Also, has the ability to resume
    if the upload is interrupted.
    """

    field_name = 'file'
    content_range_header = 'HTTP_CONTENT_RANGE'
    content_range_pattern = re.compile(
        r'^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$'
    )
    max_bytes = MAX_BYTES  # Max amount of data that can be uploaded
    # If `fail_if_no_header` is True, an exception will be raised if the
    # content-range header is not found. Default is False to match Jquery File
    # Upload behavior (doesn't send header if the file is smaller than chunk)
    fail_if_no_header = False

    def get_extra_attrs(self, request):
        """
        Extra attribute values to be passed to the new ChunkedUpload instance.
        Should return a dictionary-like object.
        """
        return {}

    def get_max_bytes(self, request):
        """
        Used to limit the max amount of data that can be uploaded. `None` means
        no limit.
        You can override this to have a custom `max_bytes`, e.g. based on
        logged user.
        """

        return self.max_bytes

    def create_chunked_upload(self, save=False, **attrs):
        """
        Creates new chunked upload instance. Called if no 'upload_id' is
        found in the POST data.
        """
        chunked_upload = self.model(**attrs)
        # file starts empty
        chunked_upload.file.save(name='', content=ContentFile(''), save=save)

        return chunked_upload

    def is_valid_chunked_upload(self, chunked_upload):
        """
        Check if chunked upload has already expired or is already complete.
        """
        if chunked_upload.expired:
            raise ChunkedUploadError(status=http_status.HTTP_410_GONE,
                                     detail='Upload has expired')
        error_msg = 'Upload has already been marked as "%s"'
        if chunked_upload.status == COMPLETE:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail=error_msg % 'complete')

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        """

        return {
            'upload_id': chunked_upload.upload_id,
            'offset': chunked_upload.offset,
            'expires': chunked_upload.expires_on
        }

    def _post(self, request, *args, **kwargs):
        chunk = request.FILES.get(self.field_name)
        if chunk is None:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail='No chunk file was submitted')
        self.validate(request)

        upload_id = request.POST.get('upload_id')
        if upload_id:
            chunked_upload = get_object_or_404(self.get_queryset(request),
                                               upload_id=upload_id)
            self.is_valid_chunked_upload(chunked_upload)
        else:
            attrs = {'filename': chunk.name}
            if hasattr(request, 'user') and request.user.is_authenticated():
                attrs['user'] = request.user
            attrs.update(self.get_extra_attrs(request))
            chunked_upload = self.create_chunked_upload(save=False, **attrs)

        content_range = request.META.get(self.content_range_header, '')
        print 'content_range'
        print content_range
        match = self.content_range_pattern.match(content_range)
        if match:
            start = int(match.group('start'))
            end = int(match.group('end'))
            total = int(match.group('total'))
        elif self.fail_if_no_header:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail='Error in request headers')
        else:
            # Use the whole size when HTTP_CONTENT_RANGE is not provided
            start = 0
            end = chunk.size - 1
            total = chunk.size

        chunk_size = end - start + 1
        max_bytes = self.get_max_bytes(request)

        if max_bytes is not None and total > max_bytes:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail='Size of file exceeds the limit (%s bytes)' % max_bytes
            )
        if chunked_upload.offset != start:
            print 'offset check; ' 
            print chunked_upload.offset
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail='Offsets do not match',
                                     offset=chunked_upload.offset)
        if chunk.size != chunk_size:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail="File size doesn't match headers")

        chunked_upload.append_chunk(chunk, chunk_size=chunk_size, save=False)

        self._save(chunked_upload)

        return Response(self.get_response_data(chunked_upload, request),
                        status=http_status.HTTP_200_OK)


class ChunkedUploadCompleteView(ChunkedUploadBaseView):
    """
    Completes an chunked upload. Method `on_completion` is a placeholder to
    define what to do when upload is complete.
    """

    # I wouldn't recommend to turn off the md5 check, unless is really
    # impacting your performance. Proceed at your own risk.
    do_md5_check = True  #False

    def on_completion(self, uploaded_file, request):
        """
        Placeholder method to define what to do when upload is complete.
        """
    def get_response_data(self, chunked_upload, request):
        return chunked_upload.filename
        #return {'message': ("%s %s " %
                            #(chunked_upload.filename, chunked_upload.offset))}


    def is_valid_chunked_upload(self, chunked_upload):
        """
        Check if chunked upload is already complete.
        """
        if chunked_upload.status == COMPLETE:
            error_msg = "Upload has already been marked as complete"
            return ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                      detail=error_msg)

    def md5_check(self, chunked_upload, md5):
        """
        Verify if md5 checksum sent by client matches generated md5.
        """
        if chunked_upload.md5 != md5:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail='md5 checksum does not match')

    def _post(self, request, *args, **kwargs):
        upload_id = request.POST.get('upload_id')
        md5 = request.POST.get('md5')

        error_msg = None
        if self.do_md5_check:
            if not upload_id or not md5:
                error_msg = "Both 'upload_id' and 'md5' are required"
        elif not upload_id:
            error_msg = "'upload_id' is required"
        if error_msg:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail=error_msg)

        chunked_upload = get_object_or_404(self.get_queryset(request),
                                           upload_id=upload_id)

        self.validate(request)
        self.is_valid_chunked_upload(chunked_upload)
        if self.do_md5_check:
            self.md5_check(chunked_upload, md5)

        chunked_upload.status = COMPLETE
        chunked_upload.completed_on = timezone.now()
        self._save(chunked_upload)
        self.on_completion(chunked_upload.get_uploaded_file(), request)

        return Response(self.get_response_data(chunked_upload, request),
                        status=http_status.HTTP_200_OK)


class ETPUploadView(ChunkedUploadView):

    model = ETPupload
    field_name = 'the_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass
        
    #def is_valid_chunked_upload(self, chunked_upload):
        
        #pass

'''  
    def save(self, chunked_upload, request, new=False):
        """
        Method that calls save(). Overriding may be useful is save() needs
        special args or kwargs.
        """
        pass
'''

class ETPUploadCompleteView(ChunkedUploadCompleteView):

    model = ETPupload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        #print uploaded_file.file
        #print 'filename: %s, type(file): %s' % (uploaded_file.name, type(uploaded_file.file))
        
        ipidfromkwargs = self.kwargs['ipid']
        ourip = get_object_or_404(InformationPackage, pk=ipidfromkwargs)
        ipcontentpath = ourip.directory + '/' + ourip.uuid + '/content/'
        print ipcontentpath
        shutil.move(uploaded_file.file.path,ipcontentpath)
        #pass



