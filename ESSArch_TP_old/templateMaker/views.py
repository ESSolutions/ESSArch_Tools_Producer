
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader, RequestContext
from models import templatePackage
#file upload
# import the logging library and get an instance of a logger
import logging
logger = logging.getLogger('code.exceptions')

import re
import shutil
import json
import os
from collections import OrderedDict

from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from esscore.template.templateGenerator.testXSDToJSON import generate


def constructContent(text):
    res = []
    i = text.find('{{')
    if i > 0:
        d = {}
        d['text'] = text[0:i]
        res.append(d)
        r = constructContent(text[i])
        for j in range(len(r)):
            res.append(r[j])
        # for (var j = 0; j < r.length; j++) {
        #     res.push(r[j]);
        # }
    elif i == -1:
        if len(text) > 0:
            d = {}
            d['text'] = text
            res.append(d)
    else:
        d = {};
        v = text[i+2:]
        i = v.find('}}')
        d['var'] = v[0:i]
        res.append(d);
        r = constructContent(v[i+2:])
        for j in range(len(r)):
            res.append(r[j])
    return res

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

#debugg only
def resetData(request):

    struc, el = generate();
    t = templatePackage(structure=struc, elements=el, name='test')
    t.save()
    return JsonResponse(struc, safe=False)

def getStruct(request, name):

    obj = get_object_or_404(templatePackage, pk=name)
    return JsonResponse(obj.structure, safe=False)

def getElement(request, name, uuid):
    obj = get_object_or_404(templatePackage, pk=name)
    j = json.loads(obj.elements, object_pairs_hook=OrderedDict)
    return JsonResponse(json.dumps(j[uuid]), safe=False)

def getDataJSON(request):
    # j = ''
    # jsonFile = os.open('/ESSArch/etp/data.json',os.O_RDWR|os.O_CREAT)
    # with open('/ESSArch/etp/data.json', 'r') as jsonFile:
    #     j = jsonFile.read()
        # TODO possibly remove all but structure info
    struc, el = generate();
    return JsonResponse(struc, safe=False)
    # return HttpResponse(j, content_type="application/json")

class create(View):
    template_name = 'templateMaker/create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # v = add.delay(4,4)
        # logger.log(v.get())
        context = {}
        # context['label'] = 'Prepare new information packages'

        # Get current site_profile and zone
        # site_profile, zone = lat.getSiteZone()

        # Present only prepared IPs
        # ip = InformationPackage.objects.filter(state='Prepared')

        # initialvalues = {}
        # initialvalues['destinationroot'] = lat.getLogFilePath()
        # if site_profile == "SE":
            # form = PrepareFormSE(initial=initialvalues) # Form with defaults
        # if site_profile == "NO":
            # form = PrepareFormNO(initial=initialvalues) # Form with defaults

        # context['form'] = form
        # context['zone'] = zone
        # context['informationpackages'] = ip
        return render(request, self.template_name, context)

class edit(View):
    template_name = 'templateMaker/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # v = add.delay(4,4)
        # logger.log(v.get())
        context = {}
        context['label'] = 'Edit template'

        # Get current site_profile and zone
        # site_profile, zone = lat.getSiteZone()

        # Present only prepared IPs
        # ip = InformationPackage.objects.filter(state='Prepared')

        # initialvalues = {}
        # initialvalues['destinationroot'] = lat.getLogFilePath()
        # if site_profile == "SE":
            # form = PrepareFormSE(initial=initialvalues) # Form with defaults
        # if site_profile == "NO":
            # form = PrepareFormNO(initial=initialvalues) # Form with defaults

        # context['form'] = form
        # context['zone'] = zone
        # context['informationpackages'] = ip
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        # 1. load elements
        # 2. find with correct uuid
        # 3. update
        # 4. save
        # return HttpResponse(json.dumps(request.POST))
        name = request.POST['schemaName']
        uuid = request.POST['uuid']

        obj = get_object_or_404(templatePackage, pk=name)
        j = json.loads(obj.elements, object_pairs_hook=OrderedDict)
        oldData = j[uuid]
        for key, value in request.POST.iteritems():
            if key.startswith('formly_'):
                # key has format formly_[form_id]_[type (input | select)]_[key]_[num] Wanted value is [key]
                end = key.rfind('_')
                k = key[0:end]
                start = k.rfind('_')
                k = k[start+1:]
                for attrib in oldData['attributes']:
                    if attrib['key'] == k:
                        v = value
                        if value.startswith('string:'):
                            v = v[7:]
                        attrib['defaultValue'] = v
                        break

        obj.elements = json.dumps(j)
        obj.save()
        return HttpResponse(obj.elements)
