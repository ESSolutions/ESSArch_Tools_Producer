"""sdf."""
# import os
# import sys
from lxml import etree
import os
import hashlib
import time
import uuid


# METS_NS = 'http://www.loc.gov/METS/'
# METSEXT_NS = 'ExtensionMETS'
# XLINK_NS = "http://www.w3.org/1999/xlink"
# METS_NSMAP = {None: METS_NS, "xlink": "http://www.w3.org/1999/xlink", "ext": METSEXT_NS,
#               "xsi": "http://www.w3.org/2001/XMLSchema-instance"}
# DELIVERY_METS_NSMAP = {None: METS_NS, "xlink": "http://www.w3.org/1999/xlink",
#    "xsi": "http://www.w3.org/2001/XMLSchema-instance"}

# M = objectify.ElementMaker(
#     annotate=False,
#     namespace=METS_NS,
#     nsmap=METS_NSMAP)

# role = "testRole"
# # type = "testType"
# other_type = "testOtherType"
# name = "testName"
# note = "testNote"
#
# mets = M.mets({"OBJID": "UUID:"})
#
# agent = M.agent({"ROLE": role, "OTHERTYPE": other_type},
#                 M.name(name), M.note(note))
# mets.agent = agent

# for i in range(0, 1000):
#     mets.append(M.file({"title":i}))
# print etree.tostring(mets, pretty_print=True)


############## ((  INFO  )) ##############

# value must NOT contaion space

# test med 50,000,000 file entries, (inte lasta ifran systemet) pa 447s.

############## ((  TODO  )) ##############

# 1. sanitize all attributes and values

# 2. indentation for pretty print

# 3. namespace


info = {"xmlns:mets": "http://www.loc.gov/METS/",
        "xmlns:ext": "ExtensionMETS",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd"
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
        "agents":[{
                "ROLE":"ARCHIVIST",
                "TYPE":"ORGANIZATION",
                "name":"Arkivbildar namn",
                "note":"VAT:SE201345098701",
            },{
                "ROLE":"ARCHIVIST",
                "TYPE":"OTHER",
                "OTHERTYPE":"SOFTWARE",
                "name":"Arkivbildar namn",
                "note":"VAT:SE201345098701",
            }],
        }

eol_ = '\n'

debug = False
pretty = True
fileElements = []
files = []
filenames = []


def dlog(string):
    if debug:
        print string


def pretty_print(fd, level, pretty):
    if pretty:
        for idx in range(level):
            os.write(fd, '    ')


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
                        # print "return True 1"
                        return True
                if self.value is not '':
                    pretty_print(fd, level + 1, pretty)
                    os.write(fd, self.value + eol_)
                pretty_print(fd, level, pretty)
                os.write(fd, '</' + self.completeTagName + '>' + eol_)
                self.printed = 2
            else:
                self.printed = 1
                # print "return True 2: " + self.completeTagName
                return True
        else:
            os.write(fd, '/>' + eol_)
            self.printed = 2

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


def create2(tree, namespace=''):
    empty = True
    t = xmlElement(tree.tag, namespace)
    if tree.text is not None:
        text = tree.text.replace('\n', '').replace(' ', '')
        if text != '':
            # print tree.text.replace('\n', '').replace(' ','')
            if text in info:
                empty = False
                t.value = info[tree.text]
    if tree.get('containsFiles') == '1':
        t.containsFiles = True
        empty = False
        fileElements.append(tree)
        if len(files) > 0:
            filenames.append("tmp" + str(len(files))+".txt")
            files.append(os.open("tmp" + str(len(files))+".txt",os.O_RDWR|os.O_CREAT))
        else:
            files.append(os.open(info['filename'],os.O_RDWR|os.O_CREAT))
        # print "found files"
    else:
        for child in tree:
            if child.tag == 'attr':
                # value = info[child.text]
                if child.get('value') is '1':
                    t.addAttribute(xmlAttribute(child.get('name'), child.text))
                else:
                    if child.text in info:
                        value = info[child.text]
                        name = child.get('name')
                        t.addAttribute(xmlAttribute(name, value))
                    else:
                        if child.get('req') == '1':
                            print "ERROR: missing required value for: " + child.text
                        else:
                            # debug
                            dlog("INFO: missing optional value for: " + child.text)
            elif child.tag == 'namespace':
                t.setNamespace(child.text)
                namespace = child.text
            else:
                c = create2(child, namespace)
                if c is not None:
                    empty = False
                    t.addChild(c)
    if empty:
        if tree.get('allowEmpty') == '1':
            return t
        else:
            return None
    else:
        return t

def checksum(filename):
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

def parseFiles(filename='/SIP/huge'):
    #'/SIP/sip test 1/metadata'
    fileInfo = {}
    #
    # for i in range(0, 10000000):
    #     fileInfo['FName'] = 'asdfsdf'
    #     fileInfo['FChecksum'] = hashlib.md5('/SIP/arc 2.tar').hexdigest() #get_sha256_hash(file_name)
    #     fileInfo['FID'] = '12'
    #     # write to file
    #     for e in fileElements:
    #         t = create3(e, fileInfo)
    #         t.printXML(3)

        #original
    for dirname, dirnames, filenames in os.walk(filename):
        print dirname
        for file in filenames:

            #populate dictionary

            fileInfo['FName'] = dirname+'/'+file
            # fileInfo['FChecksum'] = hashlib.sha256(dirname+'/'+file).hexdigest() #get_sha256_hash(file_name)
            fileInfo['FChecksum'] = checksum(dirname+'/'+file)
            fileInfo['FID'] = "ID" + uuid.uuid4().__str__()
            fileInfo['FMimetype'] = 'application/msword'
            fileInfo['FCreated'] = '2016-02-21T11:18:44+01:00'
            fileInfo['FFormatName'] = 'MS word'
            fileInfo['FSize'] = str(os.path.getsize(dirname+'/'+file))
            fileInfo['FUse'] = 'DataFile'
            fileInfo['FChecksumType'] = 'SHA256'
            fileInfo['FLoctype'] = 'URL'
            fileInfo['FLinkType'] = 'simple'
            # write to file
            for idx, e in enumerate(fileElements):
                t = create3(e[0], fileInfo)
                t.printXML(files[idx],3) # TODO change 3 to passed variable

def create3(el, fileInfo, namespace='mets'):
    empty = True
    t = xmlElement(el.tag, namespace)
    # t.printXML()
    # t.level = ?
    # print fileInfo
    if el.text is not None:
        text = el.text.replace('\n', '').replace(' ', '')
        if text != '':
            # print tree.text.replace('\n', '').replace(' ','')
            if text in fileInfo:
                empty = False
                t.value = fileInfo[el.text]
    # if el.get('containsFiles') == '1':
        # t.containsFiles = True
        # empty = False
        # print "found files"
    # else:
    for child in el:
        if child.tag == 'attr':
            # value = info[child.text]
            if child.get('value') is '1':
                t.addAttribute(xmlAttribute(child.get('name'), child.text))
            else:
                if child.text in fileInfo:
                    value = fileInfo[child.text]
                    name = child.get('name')
                    t.addAttribute(xmlAttribute(name, value))
                else:
                    if child.get('req') == '1':
                        print "ERROR: missing required value for: " + child.text
                    else:
                        # debug
                        dlog("INFO: missing optional value for: " + child.text)
        elif child.tag == 'namespace':
            t.setNamespace(child.text)
            namespace = child.text
        else:
            c = create3(child, fileInfo, namespace)
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



# def create3(tree, namespace=''):
#     empty = True
#     hasAttrib = False
#     t = xmlElement(tree.tag, namespace)
#     if tree.text is not None:
#         text = tree.text.replace('\n', '').replace(' ', '')
#         if text != '':
#             # print tree.text.replace('\n', '').replace(' ','')
#             if text in info:
#                 empty = False
#                 t.value = info[tree.text]
#     for child in tree:
#         if child.tag == 'attr':
#             # value = info[child.text]
#             if child.get('value') is '1':
#                 hasAttrib = True
#                 t.addAttribute(xmlAttribute(child.get('name'), child.text))
#             else:
#                 if child.text in info:
#                     hasAttrib = True
#                     value = info[child.text]
#                     name = child.get('name')
#                     t.addAttribute(xmlAttribute(name, value))
#                 else:
#                     if child.get('req') == '1':
#                         print "ERROR: missing required value for: " + child.text
#                     else:
#                         # debug
#                         dlog("INFO: missing optional value for: " + child.text)
#         elif child.tag == 'namespace':
#             t.setNamespace(child.text)
#             namespace = child.text
#         elif child.tag == 'files':
#             t.containsFiles = True
#         else:
#             c = create2(child, namespace)
#             if c is not None:
#                 empty = False
#                 t.addChild(c)
#     if empty:
#         if tree.get('allowEmpty') == '1':
#             return t
#         else:
#             return None
#     else:
#         return t

# parser = etree.XMLParser(remove_blank_text=True)
# pars = etree.XML(xmlFile, parser)

start = time.time()
# print str(start)

pars = etree.parse("template2.xml")
# fd = os.open("f3.txt",os.O_RDWR|os.O_CREAT)
rootEl = create2(pars.getroot())
# rootEl.printXML(fd)
if len(files) < 1:
    files.append(os.open(info['filename'],os.O_RDWR|os.O_CREAT))
if rootEl.printXML(files[0]):
    parseFiles()
    rootEl.printXML(files[0])
    #add file to bottom of sip
    f = files[0]
    for filename in filenames:
        fd = os.open(filename, os.O_RDWR)
        while True:
            data = os.read(fd, 65536)
            if data:
                os.write(f, data)
            else:
                break
        # print more XML
        rootEl.printXML(files[0])
end = time.time()
# print str(end)
print "Ended in: " + str(end - start) + "s."

    # print "files goes here \n\n\n" + str(rootEl.printed)

# print etree.tostring(root)

# e = xmlElement('mets')
# b = xmlElement('agent')
# e.addAttribute(xmlAttribute('ID', '2k3lno42'))
# e.addChild(b)
# e.printXML()
