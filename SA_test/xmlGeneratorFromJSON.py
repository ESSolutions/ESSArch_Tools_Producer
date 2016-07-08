from lxml import etree
import os
import hashlib
import uuid
import json
from collections import OrderedDict
import re

debug = False
pretty = True
eol_ = '\n'
fileElements = []
files = []
filenames = []
normalElements = []
normalFiles = []
sortedElements = []
sortedArguments = []
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

# class fileGrp():
#
#     el = None
#     fid = None
#     children = []
#
#     def __init__(self, el=None, fid=None, children=[]):
#         pass
#
#     def addChild(self, el=None, fid=None, children=[]):
#         self.children.append(fileGrp(el, fid, children))


def parseFiles(filename='/SIP/huge', level=3):
    fileInfo = {}

    # for e in fileElements:
    #     if e.attr('sortBy'):
    #         sortedElements.append(e)
    #     else:
    #         normalElements.append(e)

    for dirname, dirnames, filenames in os.walk(filename):
        # print dirname
        for file in filenames:

            #populate dictionary

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
            # write to file
            for idx, e in enumerate(normalElements):
                t = createXMLStructureForFiles(e[0], fileInfo)
                t.printXML(normalFiles[idx],level)

            for idx, e in enumerate(sortedElements):
                # test arguments
                found = True
                for key, value in sortedArguments[idx].iteritems():
                    if re.search(value, fileInfo[key]) is None:
                        found = False
                        break
                if found:
                    t = createXMLStructureForFiles(e[0], fileInfo)
                    t.printXML(sortedFiles[idx],level)

def getValue(key, info):
    if key is not None:
        text = sanitizeString(key)
        if text != '':
            # print tree.text.replace('\n', '').replace(' ','')
            if text in info:
                return info[text]
    return None

def analyzeFileStructure(tree, namespace):
    global foundFiles
    empty = True
    t = xmlElement(tree.tag, namespace)
    if tree.get('containsFiles') == '1':
        t.containsFiles = True
        empty = False
        if tree.get('sortby'):
            sortedElements.append(tree)
            filenames.append("tmp" + str(foundFiles)+".txt")
            sortedFiles.append(os.open("tmp" + str(foundFiles)+".txt",os.O_RDWR|os.O_CREAT))
            #split arguments
            reg = tree.get('sortby')
            reg = reg.split(';')
            arg = {}
            for s in reg:
                if s is not '':
                    s = s.split('=')
                    arg[s[0]] = s[1]
            sortedArguments.append(arg)
        else:
            normalElements.append(tree)
            filenames.append("tmp" + str(foundFiles)+".txt")
            normalFiles.append(os.open("tmp" + str(foundFiles)+".txt",os.O_RDWR|os.O_CREAT))
        foundFiles += 1

    for child in tree:
        ch = analyzeFileStructure(child, namespace)
        if ch is not None:
            t.addChild(ch)
            empty = False
    if not empty:
        return t


def createXMLStructure(name, content, info, namespace=''):
    global foundFiles
    t = xmlElement(name, namespace)
    # loop through all attribute and children
    if 'containsFiles' in content:

        c = {}
        for key, value in content:
            if key[:1] != '-' and key[:1] != '#':
                if key != 'attr':
                    c[key] = value

        if 'sortby' in content:
            sortedElements.append(c)
            filenames.append("tmp" + str(foundFiles)+".txt")
            sortedFiles.append(os.open("tmp" + str(foundFiles)+".txt",os.O_RDWR|os.O_CREAT))
            #split arguments
            reg = content['sortby']
            reg = reg.split(';')
            arg = {}
            for s in reg:
                if s is not '':
                    s = s.split('=')
                    arg[s[0]] = s[1]
            sortedArguments.append(arg)
        else:
            normalElements.append(c)
            filenames.append("tmp" + str(foundFiles)+".txt")
            normalFiles.append(os.open("tmp" + str(foundFiles)+".txt",os.O_RDWR|os.O_CREAT))
        foundFiles += 1

        for key, value in c:
            ch = analyzeFileStructure(key, value, namespace)
            if ch is not None:
                t.addChild(ch)
        t.containsFiles = True
    else:
        for key, value in content.iteritems():
            if key == '#content':
                for c in value:
                    if 'text' in c:
                        t.value += c['text']
                    elif 'var' in c:
                        text = getValue(c['var'], info)
                        if text is not None:
                            t.value += text
            elif key[:1] != '-':
                #child
                if key == 'attr':
                    #parse attrib children
                    for attrib in value:
                        attribute = parseAttribute(attrib, info)
                        if attribute is None:
                            if '-req' in attrib:
                                if attrib['-req'] == '1':
                                    print "ERROR: missing required value for: " + key
                                else:
                                    dlog("INFO: missing optional value for: " + key)
                            else:
                                dlog("INFO: missing optional value for: " + key)
                        else:
                            t.addAttribute(attribute)
                elif key == 'namespace':
                    t.setNamespace(value)
                    namespace = value
                else:
                    if 'arr' not in value:
                        if isinstance(value, OrderedDict):
                            c = createXMLStructure(key, value, info, namespace)
                            if c is not None:
                                t.addChild(c)
                        elif isinstance(value, list):
                            for l in value:
                                c = createXMLStructure(key, l, info, namespace)
                                if c is not None:
                                    t.addChild(c)
                    else:
                        occurrences = 1
                        if 'max' in value:
                            occurrences = int(value['max'])
                            if occurrences == -1:
                                occurrences = 10000000000 # unlikely to surpass this
                        #parse array string and pass info
                        attr = value['attr'] # TODO could be improved with JSON
                        attr = attr.split(':')
                        args = attr[1].split(',')
                        testArgs = {}
                        for s in args:
                            r = s.split('=')
                            testArgs[r[0]] = r[1]
                        dictionaries = info[attr[0]]
                        for used in xrange(0, occurrences):
                            dic = findMatchingSubDict(dictionaries, testArgs)
                            if dic is not None:
                                #done, found matching entries
                                c = createXMLStructure(key, value, dic, namespace)
                                if c is not None:
                                    t.addChild(c)
                                    dictionaries.remove(dic)
                                else:
                                    break
                            else:
                                break

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
            if dic[key] != value:
                found = False
        if found:
            return dic
    return None

def createXMLStructureForFiles(el, fileInfo, namespace='mets'):
    empty = True
    t = xmlElement(el.tag, namespace)
    text = getValue(el.text, info)
    if text is not None:
        t.value = text
        empty = False
    for child in el:
        if child.tag == 'attr':

            #parse attrib children
            attribute = parseAttribute(child, fileInfo)
            if attribute is None:
                if child.get('req') == '1':
                    print "ERROR: missing required value for: " + child.text
                else:
                    # debug
                    dlog("INFO: missing optional value for: " + child.text)
            else:
                t.addAttribute(attribute)

        elif child.tag == 'namespace':
            t.setNamespace(child.text)
            namespace = child.text
        elif child.tag == 'metsGenText':
            if child.get('name'):
                t.value += child.get('name')
        else:
            c = createXMLStructureForFiles(child, fileInfo, namespace)
            if c is not None:
                empty = False
                t.addChild(c)
    if empty:
        if el.get('allowEmpty') == '1':
            return t
        else:
            return None
    else:
        return t

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
        if self.value != '' or self.children:
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


info = {"xmlns:mets": "http://www.loc.gov/METS/",
        "xmlns:ext": "ExtensionMETS",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd "
        "ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd",
        "PROFILE": "http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xmll",
        "LABEL": "Test of SIP 1",
        "TYPE": "Personnel",
        # "mets:ID":"ID8b42fed2-c281-43b4-9798-5168126b0a4b",
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
                "note":"VAT:SE201345098701",
            },{
                "ROLE":"ARCHIVIST",
                "TYPE":"OTHER",
                "OTHERTYPE":"SOFTWARE",
                "name":"By hand Systems",
                "note":"1.0.0",
            },{
                "ROLE":"ARCHIVIST",
                "TYPE":"OTHER",
                "OTHERTYPE":"SOFTWARE",
                "name":"Other By hand Systems",
                "note":"1.2.0",
            }],
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

json_data=open('JSONTemplate.txt').read()

data = json.loads(json_data, object_pairs_hook=OrderedDict)
# pprint(data)
rootE = data['mets']
# for el, val in rootE.iteritems():
#     print el
xmlFile = os.open(info['filename'],os.O_RDWR|os.O_CREAT)
rootEl = createXMLStructure('mets', rootE, info)
rootEl.printXML(xmlFile)
