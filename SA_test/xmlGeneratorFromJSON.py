# from lxml import etree
import os
import hashlib
import uuid
import json
from collections import OrderedDict
import re
import copy

debug = False
pretty = True
eol_ = '\n'
# fileElements = []
# files = []
# filenames = []
# normalElements = []
# normalFiles = []
# sortedElements = []
# sortedArguments = []
sortedFiles = []
foundFiles = 0
xmlFile = ''

def dlog(string):
    if debug:
        print string


def pretty_print(fd, level, pretty):
    if pretty:
        for idx in range(level):
            os.write(fd, '    ')

def calculateChecksum(filename):
    fd = os.open(filename, os.O_RDONLY)
    hashSHA = hashlib.sha256()
    while True:
        data = os.read(fd, 65536)
        if data:
            hashSHA.update(data)
        else:
            break
    os.close(fd)
    return hashSHA.hexdigest()

def sanitizeString(s):
    return s.rstrip()

def parseFiles(filename='/SIP/huge', level=3):
    fileInfo = {}

    for dirname, dirnames, filenames in os.walk(filename):
        # print dirname
        for file in filenames:

            # populate dictionary

            fileInfo['FName'] = dirname+'/'+file
            fileInfo['FChecksum'] = calculateChecksum(dirname+'/'+file)
            fileInfo['FID'] = uuid.uuid4().__str__()
            fileInfo['FMimetype'] = 'application/msword'
            fileInfo['FCreated'] = '2016-02-21T11:18:44+01:00'
            fileInfo['FFormatName'] = 'MS word'
            fileInfo['FSize'] = str(os.path.getsize(dirname+'/'+file))
            fileInfo['FUse'] = 'DataFile'
            fileInfo['FChecksumType'] = 'SHA-256'
            fileInfo['FLoctype'] = 'URL'
            fileInfo['FLinkType'] = 'simple'
            fileInfo['FChecksumLib'] = 'hashlib'
            fileInfo['FLocationType'] = 'URI'
            fileInfo['FIDType'] = 'UUID'
            # write to file

            for fi in sortedFiles:
                for fil in fi.files:
                    if not fil.arguments:
                        for key, value in fil.element.iteritems():
                            t = createXMLStructure(key, value, fileInfo)
                            t.printXML(fil.fid,fil.level)
                    else:
                        found = True
                        for key, value in fil.arguments.iteritems():
                            if re.search(value, fileInfo[key]) is None:
                                found = False
                                break
                        if found:
                            for key, value in fil.element.iteritems():
                                t = createXMLStructure(key, value, fileInfo)
                                t.printXML(fil.fid,fil.level)

def getValue(key, info):
    if key is not None:
        text = sanitizeString(key)
        if text != '':
            # print tree.text.replace('\n', '').replace(' ','')
            if text in info:
                return info[text]
    return None

def analyzeFileStructure(name, content, namespace, fob, t=None, level=0):
    global foundFiles
    if t is None:
        t = xmlElement(name, namespace)
    if '-containsFiles' in content:
        t.containsFiles = True
        c = content['-containsFiles']
        arg = None
        if isinstance(c, OrderedDict):
            con = {}
            for key, value in c.iteritems():
                if key[:1] != '-' and key[:1] != '#':
                    con[key] = value
            if '-sortby' in c:
                arg = c['-sortby']
            f = fileInfo(con, "tmp" + str(foundFiles)+".txt", arg)
            f.fid = os.open(f.filename,os.O_RDWR|os.O_CREAT)
            f.level = level
            fob.files.append(f)
            for key, value in con.iteritems():
                if key[:1] != '-' and key[:1] != '#':
                    ch = analyzeFileStructure(key, value, namespace, fob, level=level+1)
                    if ch is not None:
                        t.addChild(ch)

        elif isinstance(c, list):
            for co in c:
                con = {}
                for key, value in co.iteritems():
                    if key[:1] != '-' and key[:1] != '#':
                        con[key] = value
                if '-sortby' in co:
                    arg = co['-sortby']
                f = fileInfo(con, "tmp" + str(foundFiles)+".txt", arg)
                f.fid = os.open(f.filename,os.O_RDWR|os.O_CREAT)
                f.level = level
                fob.files.append(f)
            foundFiles += 1

            for key, value in con.iteritems():
                if key[:1] != '-' and key[:1] != '#':
                    ch = analyzeFileStructure(key, value, namespace, fob, level=level+1)
                    if ch is not None:
                        t.addChild(ch)
        foundFiles += 1
    if t.containsFiles:
        return t
    else:
        return None

def parseChild(name, content, info, namespace, t, fob, level=0):
    if '-arr' not in content:
        c = createXMLStructure(name, content, info, fob, namespace, level+1)
        if c is not None:
            t.addChild(c)
    else:
        occurrences = 1
        if '-max' in content:
            occurrences = int(content['-max'])
            if occurrences == -1:
                occurrences = 10000000000 # unlikely to surpass this
        #parse array string and pass info
        attr = content['-arr'] # TODO could be improved with JSON
        attr = attr.split(':')
        args = attr[1].split(',')
        testArgs = {}
        for s in args:
            r = s.split('=')
            testArgs[r[0]] = r[1]
        dictionaries = copy.deepcopy(info[attr[0]])
        for used in xrange(0, occurrences):
            dic = findMatchingSubDict(dictionaries, testArgs)
            if dic is not None:
                #done, found matching entries
                c = createXMLStructure(name, content, dic, fob, namespace, level+1)
                if c is not None:
                    t.addChild(c)
                    dictionaries.remove(dic)
                else:
                    break
            else:
                break


def createXMLStructure(name, content, info, fob=None, namespace='', level=1):
    global foundFiles
    t = xmlElement(name, namespace)
    # loop through all attribute and children
    if '-containsFiles' in content and fob is not None:
        analyzeFileStructure(name, content, namespace, fob, t, level)
    for key, value in content.iteritems():
        if key == '#content':
            for c in value:
                if 'text' in c:
                    t.value += c['text']
                elif 'var' in c:
                    text = getValue(c['var'], info)
                    if text is not None:
                        t.value += text
        elif key == '-attr':
            #parse attrib children
            for attrib in value:
                attribute = parseAttribute(attrib, info)
                if attribute is None:
                    if '-req' in attrib:
                        if attrib['-req'] == '1':
                            print "ERROR: missing required value for element: " + name + " and attribute: " + attrib['-name']
                        else:
                            dlog("INFO: missing optional value for: " + attrib['-name'])
                    else:
                        dlog("INFO: missing optional value for: " + attrib['-name'])
                else:
                    t.addAttribute(attribute)
        elif key == '-namespace':
            t.setNamespace(value)
            namespace = value
        elif key[:1] != '-':
            #child
            if isinstance(value, OrderedDict):
                parseChild(key, value, info, namespace, t, fob, level)
            elif isinstance(value, list):
                for l in value:
                    parseChild(key, l, info, namespace, t, fob, level)

    if t.isEmpty():
        if  '-allowEmpty' in content:
            if content['-allowEmpty'] != '1':
                return None
            else:
                return t
        else:
            return None
    else:
        return t

def findMatchingSubDict(dictionaries, testValue):
    for dic in dictionaries:
        # compare agent dicts
        found = True
        for key, value in testValue.iteritems():
            if key in dic:
                if dic[key] != value:
                    found = False
            else:
                found = False
        if found:
            return dic
    return None

def parseAttribute(content, info):
    text = ''
    name = content['-name']
    for c in content['#content']:
        if 'text' in c:
            text += c['text']
        elif 'var' in c:
            t = getValue(c['var'], info)
            if t is not None:
                text += t
    if text is not '':
        return xmlAttribute(name, text)
    else:
        return None

class xmlAttribute(object):
    '''
    dsf.
    '''
    attrName = ''
    req = False
    value = ''

    def __init__(self, attrName, value=''):
        self.attrName = attrName
        self.value = value

    def printXML(self, fd):
        if self.value is not '':
            os.write(fd, ' ' + self.attrName + '="' + self.value + '"')

class xmlElement(object):
    '''
    dsf.
    '''

    def __init__(self, tagName='', namespace=''):
        self.tagName = tagName
        self.children = []
        self.attributes = []
        self.value = ''
        self.karMin = 0
        self.karMax = -1
        self.namespace = namespace
        self.completeTagName = ''
        self.containsFiles = False
        self.printed = 0
        if self.namespace != '':
            self.completeTagName += self.namespace + ':'
        self.completeTagName += str(self.tagName)

    def setNamespace(self, namespace):
        self.namespace = namespace
        self.completeTagName = ''
        if self.namespace != '':
            self.completeTagName += self.namespace + ':'
        self.completeTagName += self.tagName

    def printXML(self, fd, level=0):
        # if self.containsFiles:
            # print "contaions iles: " + self.tagName
        if self.printed == 2:
            return False
        if self.printed == 0:
            pretty_print(fd, level, pretty)
            os.write(fd, '<' + self.completeTagName)
            for a in self.attributes:
                a.printXML(fd)
        if self.children or self.value is not '' or self.containsFiles:
            if self.printed == 0:
                os.write(fd, '>' + eol_)
            if not self.containsFiles or self.printed == 1:
                for child in self.children:
                    if child.printXML(fd, level + 1):
                        self.printed = 1
                        return True
                if self.value is not '':
                    pretty_print(fd, level + 1, pretty)
                    os.write(fd, self.value + eol_)
                pretty_print(fd, level, pretty)
                os.write(fd, '</' + self.completeTagName + '>' + eol_)
                self.printed = 2
            else:
                self.printed = 1
                return True
        else:
            os.write(fd, '/>' + eol_)
            self.printed = 2

    def isEmpty(self):
        if self.value != '' or self.children or self.containsFiles:
            return False
        else:
            return True

    def printDebug(self):
        print self.tagName
        for child in self.children:
            child.printDebug()

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

    def addChild(self, el):
        if el.namespace == '':
            el.setNamespace(self.namespace)
        self.children.append(el)

inputData = {
    "info": {
        "xmlns:mets": "http://www.loc.gov/METS/",
                "xmlns:ext": "ExtensionMETS",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd "
                "ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd",
                "xsi:schemaLocationPremis": "http://www.loc.gov/premis/v3 https://www.loc.gov/standards/premis/premis.xsd",
                "PROFILE": "http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xmll",
                "LABEL": "Test of SIP 1",
                "TYPE": "Personnel",
                "OBJID": "UUID:9bc10faa-3fff-4a8f-bf9a-638841061065",
                "ext:CONTENTTYPESPECIFICATION": "FGS Personal, version 1",
                "CREATEDATE": "2016-06-08T10:44:00+02:00",
                "RECORDSTATUS": "NEW",
                "ext:OAISTYPE": "SIP",
                "agentName": "name",
                "agentNote": "note",
                "REFERENCECODE": "SE/RA/123456/24/F",
                "SUBMISSIONAGREEMENT": "RA 13-2011/5329, 2012-04-12",
                "MetsIdentifier": "sip.xml",
                "filename":"sip.txt",
                "SMLabel":"Profilestructmap",
                "amdLink":"IDce745fec-cfdd-4d14-bece-d49e867a2487",
                "digiprovLink":"IDa32a20cb-5ff8-4d36-8202-f96519154de2",
                "LOCTYPE":"URL",
                "MDTYPE":"PREMIS",
                "xlink:href":"file:///metadata/premis.xml",
                "xlink:type":"simple",
                "ID":"ID31e51159-9280-44d1-b26c-014077f8eeb5",
                "agents":[{
                        "ROLE":"ARCHIVIST",
                        "TYPE":"ORGANIZATION",
                        "name":"Arkivbildar namn",
                        "note":"VAT:SE201345098701"
                    },{
                        "ROLE":"ARCHIVIST",
                        "TYPE":"OTHER",
                        "OTHERTYPE":"SOFTWARE",
                        "name":"By hand Systems",
                        "note":"1.0.0"
                    },{
                        "ROLE":"ARCHIVIST",
                        "TYPE":"OTHER",
                        "OTHERTYPE":"SOFTWARE",
                        "name":"Other By hand Systems",
                        "note":"1.2.0"
                    },{
                        "ROLE":"CREATOR",
                        "TYPE":"ORGANIZATION",
                        "name":"Arkivbildar namn",
                        "note":"HSA:SE2098109810-AF87"
                    },{
                        "ROLE":"OTHER",
                        "OTHERROLE":"PRODUCER",
                        "TYPE":"ORGANIZATION",
                        "name":"Sydarkivera",
                        "note":"HSA:SE2098109810-AF87"
                    },{
                        "ROLE":"OTHER",
                        "OTHERROLE":"SUBMITTER",
                        "TYPE":"ORGANIZATION",
                        "name":"Arkivbildare",
                        "note":"HSA:SE2098109810-AF87"
                    },{
                        "ROLE":"IPOWNER",
                        "TYPE":"ORGANIZATION",
                        "name":"Informations agare",
                        "note":"HSA:SE2098109810-AF87"
                    },{
                        "ROLE":"EDITOR",
                        "TYPE":"ORGANIZATION",
                        "name":"Axenu",
                        "note":"VAT:SE9512114233"
                    },{
                        "ROLE":"CREATOR",
                        "TYPE":"INDIVIDUAL",
                        "name":"Simon Nilsson",
                        "note":"0706758942, simonseregon@gmail.com"
                    }],
    },
    "filesToCreate": {
    "sip.txt":"JSONTemplate.txt",
    "premis.txt":"JSONPremisTemplate.txt",
    "sip2.txt":"JSONTemplate.txt"
    },
    "folderToParse":"/SIP/huge/csv/000"
}

#testing

# from itertools import chain
#
# pars = etree.parse('tt.xml')
# node = pars.getroot()
# def strin(node):
#     parts = ([node.text] +
#                 list(chain(*([c.text, strin(c), c.tail] for c in node.getchildren()))) +
#                 [node.tail])
#     return parts
# print strin(node)
#
# for child in node.getchildren():
#     print child.tail

#REAL
# import time
# start = time.time()
#
# os.remove('sip.txt')
# os.remove('tmp0.txt')
# os.remove('tmp1.txt')
# os.remove('tmp2.txt')
# os.remove('tmp3.txt')
# templatename = 'template.xml'
# pars = etree.parse(templatename)
# rootEl = createXMLStructure(pars.getroot(), info)
# xmlFile = os.open(info['filename'],os.O_RDWR|os.O_CREAT)
# parseFiles('/SIP/huge/csv/000')
# if rootEl.printXML(xmlFile):
#     # rootEl.printXML(xmlFile)
#     #add file to bottom of xml
#     for filename in filenames:
#         # add tmp file to end of xml
#         fd = os.open(filename, os.O_RDONLY)
#         while True:
#             data = os.read(fd, 65536)
#             if data:
#                 os.write(xmlFile, data)
#             else:
#                 break
#         # print more XML
#         rootEl.printXML(xmlFile)
#     pass
#
# end = time.time()
# print (end - start)

# json

class fileInfo():
    # element = {}
    # filename = ''
    # arguments = {}
    # fid = None
    # level = 0

    def __init__(self, element, filename, arguments={}, level=0):
        self.element = element
        self.filename = filename
        self.arguments = arguments
        self.level = level

class fileObject():

    # files = []
    # fid = None
    # xmlFileName = ''
    # template = ''

    def __init__(self, xmlFileName, template, fid):
        self.xmlFileName = xmlFileName
        self.template = template
        self.fid = fid
        self.files = []
        self.rootElement = None


# sortedFiles = {"sip.txt":{"fid":"test","files":[{"file":"tmp0.txt", "arguments":"arg..."}]}}

# fileToCreate = {
#     "sip.txt":"JSONTemplate.txt",
#     "premis.txt":"JSONPremisTemplate.txt",
#     "sip2.txt":"JSONTemplate.txt",
# }

rootElements = []
# key = 'sip.txt'
# value = 'JSONTemplate.txt'
for key, value in inputData['filesToCreate'].iteritems():
    json_data=open(value).read()
    data = json.loads(json_data, object_pairs_hook=OrderedDict)
    name, rootE = data.items()[0] # root element
    xmlFile = os.open(key,os.O_RDWR|os.O_CREAT)
    fob = fileObject(key, value, xmlFile)
    sortedFiles.append(fob)
    rootEl = createXMLStructure(name, rootE, inputData['info'], fob)
    rootEl.printXML(xmlFile)
    fob.rootElement = rootEl

parseFiles(inputData['folderToParse'])

for fob in sortedFiles:
    for fin in fob.files:
        f = os.open(fin.filename, os.O_RDONLY)
        while True:
            data = os.read(f, 65536)
            if data:
                os.write(fob.fid, data)
            else:
                break
        # print more XML
        fob.rootElement.printXML(fob.fid)
        os.close(f)
        os.remove(fin.filename)

# for key, value in sortedFiles.iteritems():
#     for dic in value:
#         # add tmp file to end of xml
#         fd = os.open(dic['file'], os.O_RDONLY)
#         while True:
#             data = os.read(fd, 65536)
#             if data:
#                 os.write(key, data)
#             else:
#                 break
#         # print more XML
#         rootEl.printXML(xmlFile)


# json_data=open('JSONTemplate.txt').read()
#
# data = json.loads(json_data, object_pairs_hook=OrderedDict)
# # pprint(data)
# rootE = data['mets']
# # for el, val in rootE.iteritems():
# #     print el
# xmlFile = os.open(info['filename'],os.O_RDWR|os.O_CREAT)
# rootEl = createXMLStructure('mets', rootE, info)
# parseFiles('/SIP/huge/csv/000')
# if rootEl.printXML(xmlFile):
#     # rootEl.printXML(xmlFile)
#     #add file to bottom of xml
    # for filename in filenames:
    #     # add tmp file to end of xml
    #     fd = os.open(filename, os.O_RDONLY)
    #     while True:
    #         data = os.read(fd, 65536)
    #         if data:
    #             os.write(xmlFile, data)
    #         else:
    #             break
    #     # print more XML
    #     rootEl.printXML(xmlFile)
    # pass
# for filename in filenames:
#     os.remove(filename)
