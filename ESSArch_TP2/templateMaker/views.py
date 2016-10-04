
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context, loader, RequestContext
from models import templatePackage, extensionPackage
from profiles.models import Profile
import os
from django.conf import settings
#file upload
# import the logging library and get an instance of a logger
import logging
logger = logging.getLogger('code.exceptions')

# import re
import copy
import json
import uuid
from collections import OrderedDict

from django.views.generic import View
from django.http import JsonResponse
from esscore.template.templateGenerator.testXSDToJSON import generateJsonRes, generateExtensionRef
from forms import AddTemplateForm


def constructContent(text):
    res = []
    i = text.find('{{')
    if i > 0:
        d = {}
        d['text'] = text[0:i]
        res.append(d)
        r = constructContent(text[i:])
        for j in range(len(r)):
            res.append(r[j])
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

def generateElement(elements, currentUuid, takenNames=[], containsFiles=False, namespace=''):
    element = elements[currentUuid]
    el = OrderedDict()
    forms = []
    data = {}
    el['-min'] = element['min']
    el['-max'] = element['max']
    if 'namespace' in element:
        if element['namespace'] != namespace:
            namespace = element['namespace']
            el['-namespace'] = namespace
    # TODO namespace
    attributes = element['form'] + element['userForm']
    attributeList = []
    for attrib in attributes:
        # return attrib
        if attrib['key'] == '#content':
            if attrib['key'] in element['formData']:
                el['#content'] = constructContent(element['formData'][attrib['key']])
                if not containsFiles:
                    for part in el['#content']:
                        if 'var' in part:
                            # add form entry for element
                            # ?? add information of parent? example: note for agent with role=Archivist&&typ=organization (probably not needed)
                            # adding text if there occures at least one variable.
                            field = {}
                            key = part['var'] # check for doubles
                            if key in takenNames:
                                index = 0
                                while (key + str(index)) in takenNames:
                                    index += 1
                                field['key'] = (key + str(index))
                                takenNames.append((key + str(index)))
                            else:
                                field['key'] = key
                                takenNames.append(key)
                            field['type'] = 'input'
                            to = {}
                            to['type'] = 'text'
                            to['label'] = part['var']
                            field['templateOptions'] = to
                            forms.append(field)
                            data[field['key']] = ''
            else:
                el['#content'] = [] # TODO warning, should not be added if it can't contain any value
        else:
            att = OrderedDict()
            att['-name'] = attrib['key']
            att['-req'] = 0
            if 'required' in attrib['templateOptions']:
                if attrib['templateOptions']['required']:
                    att['-req'] = 1
            if attrib['key'] in element['formData']:
                att['#content'] = constructContent(element['formData'][attrib['key']])
                if not containsFiles:
                    for part in att['#content']:
                        if 'var' in part:
                            # add form entry for element
                            # ?? add information of parent? example: note for agent with role=Archivist&&typ=organization (probably not needed)
                            # adding text if there occures at least one variable.
                            field = {}
                            key = part['var'] # check for doubles
                            if key in takenNames:
                                index = 0
                                while (key + str(index)) in takenNames:
                                    index += 1
                                field['key'] = (key + str(index))
                                takenNames.append((key + str(index)))
                            else:
                                field['key'] = key
                                takenNames.append(key)
                            field['type'] = 'input'

                            to = {}
                            to['type'] = 'text'
                            to['label'] = part['var']

                            if 'desc' in attrib:
                                to['desc'] = attrib['desc']

                            if 'hideExpression' in attrib:
                                field['hideExpression'] = str(attrib['hideExpression']).lower()

                            if 'readonly' in attrib:
                                to['readonly'] = attrib['readonly']

                            field['templateOptions'] = to
                            forms.append(field)
                            data[field['key']] = ''
            else:
                att['#content'] = [] # TODO warning, should not be added if it can't contain any value
            attributeList.append(att)
    el['-attr'] = attributeList
    for child in element['children']:
        if not elements[child['uuid']]['containsFiles']:
            e, f, d = generateElement(elements, child['uuid'], takenNames, containsFiles=containsFiles, namespace=namespace)
            if e is not None:
                if child['name'] in el:
                    # cerate array
                    if isinstance(el[child['name']], list):
                        el[child['name']].append(e)
                    else:
                        temp = el[child['name']]
                        el[child['name']] = []
                        el[child['name']].append(temp)
                        el[child['name']].append(e)
                else:
                    el[child['name']] = e
                for field in f:
                    forms.append(field)
                data.update(d)
        else:
            #containsFiles
            cf = []
            elDict = OrderedDict()
            e, f, d = generateElement(elements, child['uuid'], takenNames, containsFiles=True, namespace=namespace)
            if e is not None:
                if child['name'] in elDict:
                    # cerate array
                    if isinstance(elDict[child['name']], list):
                        elDict[child['name']].append(e)
                    else:
                        temp = elDict[child['name']]
                        elDict[child['name']] = []
                        elDict[child['name']].append(temp)
                        elDict[child['name']].append(e)
                else:
                    elDict[child['name']] = e
            cf.append(elDict)
            el['-containsFiles'] = cf
    return (el, forms, data)

def generateTemplate(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    existingElements = obj.existingElements
    jsonString = OrderedDict()
    jsonString[existingElements['root']['name']], forms, data = generateElement(existingElements, 'root')

    t = finishedTemplate(name='test', template=jsonString, form=forms, data=data)
    t.save()
    return JsonResponse(jsonString, safe=False)

def getExistingElements(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    return JsonResponse(obj.existingElements, safe=False)

def getAllElements(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    return JsonResponse(obj.allElements, safe=False)

def getElements(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    res = []
    for extension in obj.extensions.all():
        if extension.existingElements != None and len(extension.existingElements) > 0:
            r = {}
            r['name'] = extension.namespace
            children = []
            for child in extension.existingElements:
                c = {}
                c['name'] = child
                c['data'] = extension.existingElements[child]
                children.append(c)
            r['children'] = children
            res.append(r)
    return JsonResponse(res, safe=False)

def removeChild(request, name, uuid):
    obj = get_object_or_404(templatePackage, pk=name)
    existingElements = obj.existingElements
    oldElement = existingElements[uuid]

    parent = existingElements[oldElement['parent']]
    index = 0
    for child in parent['children']:
        if child['uuid'] == uuid:
            del parent['children'][index]
        index += 1
    removeChildren(existingElements, oldElement)
    del existingElements[uuid]
    obj.save()
    return JsonResponse(existingElements, safe=False)

def removeChildren(existingElements ,element):
    for child in element['children']:
        removeChildren(existingElements, existingElements[child['uuid']])
        del existingElements[child['uuid']]

def addUserChild(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    newUuid = uuid.uuid4().__str__()
    res = json.loads(request.body)
    parent = obj.existingElements[res['parent']]
    element = {}
    element['anyAttribute'] = True
    element['anyElement'] = True
    element['avaliableChildren'] = []
    element['children'] = []
    element['containsFiles'] = False
    element['form'] = []
    element['formData'] = []
    element['max'] = res['max']
    element['min'] = res['min']
    element['name'] = res['name']
    element['namespace'] = parent['namespace']
    element['parent'] = res['parent']
    element['userForm'] = []
    obj.existingElements[newUuid] = element
    e = {}
    e['name'] = res['name']
    e['uuid'] = newUuid
    obj.existingElements[res['parent']]['children'].append(e)
    obj.save()
    return JsonResponse(obj.existingElements, safe=False)

def addExtensionElement(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    newUuid = uuid.uuid4().__str__()
    res = json.loads(request.body)
    parent = obj.existingElements[res['parent']]
    element = {}
    element['anyAttribute'] = True
    element['anyElement'] = True
    element['avaliableChildren'] = []
    if 'avaliableChildren' in res:
        element['avaliableChildren'] = res['avaliableChildren']
    element['children'] = []
    element['containsFiles'] = False
    element['form'] = []
    if 'form' in res:
        element['form'] = res['form']
    element['formData'] = []
    if 'formData' in res:
        element['formData'] = res['formData']
    element['max'] = res['max']
    element['min'] = res['min']
    element['name'] = res['name']
    if 'namespace' not in res:
        element['namespace'] = parent['namespace']
    else:
        element['namespace'] = res['namespace']
    element['parent'] = res['parent']
    element['userForm'] = []
    obj.existingElements[newUuid] = element
    e = {}
    e['name'] = res['name']
    e['uuid'] = newUuid
    obj.existingElements[res['parent']]['children'].append(e)
    obj.save()
    return JsonResponse(obj.existingElements, safe=False)

def addChild(request, name, newElementName, elementUuid):
    obj = get_object_or_404(templatePackage, pk=name)
    existingElements = obj.existingElements
    templates = obj.allElements
    newUuid = uuid.uuid4().__str__()
    if newElementName in templates:
        newElement = copy.deepcopy(templates[newElementName])
    else:
        for extension in obj.extensions.all():
            if newElementName in extension.allElements:
                newElement = copy.deepcopy(extension.allElements[newElementName])
    newElement['parent'] = elementUuid
    existingElements[newUuid] = newElement

    #calculate which elements should be before
    cb = calculateChildrenBefore(existingElements[elementUuid]['avaliableChildren'], newElementName)

    index = 0
    for child in existingElements[elementUuid]['children']:
        if child['name'] not in cb:
            break
        else:
            index += 1

    e = {}
    e['name'] = newElementName
    e['uuid'] = newUuid
    existingElements[elementUuid]['children'].insert(index, e)
    obj.save()
    return JsonResponse(existingElements, safe=False)

def calculateChildrenBefore(children, newElementName):
    arr = []
    for child in children:
        if child['type'] == 'element':
            if child['name'] != newElementName:
                arr.append(child['name'])
            else:
                return arr
        elif child['type'] == 'choise':
            arr = arr + calculateChildrenBefore(child['elements'], newElementName)
    return arr

def getAttributes(request, name):
    obj = get_object_or_404(templatePackage, pk=name)
    res = []
    for extension in obj.extensions.all():
        if extension.allAttributes != None and len(extension.allAttributes) > 0:
            r = {}
            r['name'] = extension.namespace
            children = []
            for child in extension.allAttributes:
                c = {}
                c['name'] = child
                c['data'] = extension.allAttributes[child]
                children.append(c)
            r['children'] = children
            res.append(r)
    return JsonResponse(res, safe=False)

def addAttribute(request, name, uuid):
    obj = get_object_or_404(templatePackage, pk=name)
    obj.existingElements[uuid]['userForm'].append(json.loads(request.body))
    obj.save()
    return JsonResponse(obj.existingElements[uuid]['userForm'], safe=False)

def setContainsFiles(request, name, uuid, containsFiles):
    obj = get_object_or_404(templatePackage, pk=name)
    if containsFiles == '1':
        obj.existingElements[uuid]['containsFiles'] = True
    else:
        obj.existingElements[uuid]['containsFiles'] = False
    obj.save()
    return JsonResponse(obj.existingElements, safe=False)

def getForm(request, name):
    obj = get_object_or_404(finishedTemplate, pk=name)
    return JsonResponse(obj.form, safe=False)

def getData(request, name):
    obj = get_object_or_404(finishedTemplate, pk=name)
    return JsonResponse(obj.data, safe=False)

def saveForm(request, name):

    res = json.loads(request.body)
    uuid = res['uuid']
    del res['uuid']

    obj = get_object_or_404(templatePackage, pk=name)
    j = obj.existingElements
    obj.existingElements[uuid]['formData'] = res
    obj.save()
    return JsonResponse(res, safe=False)

def deleteTemplate(request, name):
    if request.method == 'POST':
        templatePackage.objects.get(pk=name).delete()
        return HttpResponse('deleted')
    else:
        return HttpResponse('Error this page is only avaliable as post')

class index(View):
    template_name = 'templateMaker/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'hello World'
        objs = templatePackage.objects.all()#.values('name')
        context['templates'] = objs

        return render(request, self.template_name, context)

class add(View):
    template_name = 'templateMaker/add.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Add template'
        context['form'] = AddTemplateForm()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = AddTemplateForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(request.FILES['file'].name + ' did not success in uploading')

        name = request.POST['template_name']
        # name.replace(' ', '_')
        if templatePackage.objects.filter(pk=name).exists():
            return HttpResponse('ERROR: templatePackage with name "' + name + '" already exists!')

        existingElements, allElements = generateJsonRes(request.FILES['file'], request.POST['root_element'], request.POST['namespace_prefix']);
        t = templatePackage(existingElements=existingElements, allElements=allElements, name=name, namespace=request.POST['namespace_prefix'], root_element=request.POST['root_element'])
        t.save()
        extensionElements, extensionAll, attributes = generateExtensionRef(os.path.join(settings.BASE_DIR, 'esscore/template/templateGenerator/premis.xsd'), 'premis')
        e = extensionPackage(namespace='premis', allElements=extensionAll, existingElements=extensionElements, allAttributes=attributes)
        e.save()
        t.extensions.add(e)

        extensionElements, extensionAll, attributes = generateExtensionRef(os.path.join(settings.BASE_DIR, 'esscore/template/templateGenerator/xlink.xsd'), 'xlink')
        e = extensionPackage(namespace='xmlns', allElements=extensionAll, existingElements=extensionElements, allAttributes=attributes)
        e.save()
        t.extensions.add(e)
        # return JsonResponse(attributes, safe=False)

        t.save()
        return redirect('/template/edit/' + name)

class generate(View):
    template_name = 'templateMaker/generate.html'

    def get(self, request, *args, **kwargs):

        context = {}
        context['templateName'] = kwargs['name']

        return render(request, self.template_name, context)

    def addExtraAttribute(self, field, data, attr):
        """
        Adds extra attrbute to field if it exists in data

        Args:
            field: The field to add to
            data: The data dictionary to look in
            attr: The name of the attribute to add

        Returns:
            The new field with the attribute added to it if the attribute
            exists in data. Otherwise the original field.
        """

        field_attr = field['key'] + '_' + attr

        if field_attr in data:
            field[attr] = data[field_attr]

        return field

    def post(self, request, *args, **kwargs):
        # return JsonResponse(request.body, safe=False)
        obj = get_object_or_404(templatePackage, pk=kwargs['name'])
        existingElements = obj.existingElements

        form = existingElements['root']['form']
        formData = existingElements['root']['formData']

        for idx, field in enumerate(form):
            field = self.addExtraAttribute(field, formData, 'desc')
            field = self.addExtraAttribute(field, formData, 'hideExpression')
            field = self.addExtraAttribute(field, formData, 'readonly')

            form[idx] = field


        existingElements['root']['form'] = form

        jsonString = OrderedDict()
        jsonString[existingElements['root']['name']], forms, data = generateElement(existingElements, 'root')

        j = json.loads(request.body)
        t = Profile(profile_type=j['profile_type'],
                    name=j['name'], type=j['type'],
                    status=j['status'], label=j['label'],
                    representation_info=j['representation_info'],
                    preservation_descriptive_info=j['preservation_descriptive_info'],
                    supplemental=j['supplemental'],
                    access_constraints=j['access_constraints'],
                    datamodel_reference=j['datamodel_reference'],
                    additional=j['additional'],
                    submission_method=j['submission_method'],
                    submission_schedule=j['submission_schedule'],
                    submission_data_inventory=j['submission_data_inventory'],
                    template=forms, specification=jsonString, specification_data=data)
        t.save()
        return JsonResponse(t.specification_data, safe=False)


class demo(View):
    template_name = 'templateMaker/demo.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Edit template'

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        res = json.loads(request.body)

        obj = get_object_or_404(finishedTemplate, pk='test') # TODO not hardcoded
        obj.data = res
        obj.save()

        return JsonResponse(request.body, safe=False)

class create(View):
    template_name = 'templateMaker/create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

class edit(View):
    template_name = 'templateMaker/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        context['label'] = 'Edit template'
        context['templateName'] = kwargs['name']
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        res = json.loads(request.body)
        uuid = res['uuid']
        del res['uuid']

        obj = get_object_or_404(templatePackage, pk=kwargs['name'])
        j = obj.existingElements
        obj.existingElements[uuid]['formData'] = res
        obj.save()
        return JsonResponse(res, safe=False)