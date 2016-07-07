from lxml import etree
import os
import hashlib
import uuid

debug = False
pretty = True
eol_ = '\n'
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

def parseFiles(filename='/SIP/huge/corp', level=3):
    fileInfo = {}
    for dirname, dirnames, filenames in os.walk(filename):
        print dirname
        for file in filenames:

            #populate dictionary

            fileInfo['FName'] = dirname+'/'+file
            fileInfo['FChecksum'] = calculateChecksum(dirname+'/'+file)
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
                t = createXMLStructureForFiles(e[0], fileInfo)
                t.printXML(files[idx],level)

def createXMLStructure(tree, info, namespace=''):
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
                if child.get('arr') is None:
                    c = createXMLStructure(child, info, namespace)
                    if c is not None:
                        empty = False
                        t.addChild(c)
                else:
                    occurrences = 1
                    if child.get('max'):
                        occurrences = int(child.get('max'))
                    if occurrences == -1:
                        occurrences = 10000000000 # unlikely to surpass this
                    #parse array string and pass info
                    attr = child.get('arr')
                    attr = attr.split(':')
                    args = attr[1].split(',')
                    testArgs = {}
                    for s in args:
                        r = s.split('=')
                        testArgs[r[0]] = r[1]
                    dictionaries = info[attr[0]]
                    for used in xrange(0, 100000000):
                        print "test1"
                        dic = findMatchingSubDict(dictionaries, testArgs)
                        print "test2"
                        if dic is not None:
                            #done, found matching entries
                            c = createXMLStructure(child, dic, namespace)
                            if c is not None:
                                empty = False
                                t.addChild(c)
                                dictionaries.remove(dic)
                            else:
                                print 'break'
                                break
                        else:
                            print 'break'
                            break


    if empty:
        if tree.get('allowEmpty') == '1':
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
            f = False
            for k, v in dic.iteritems():
                if key == k and value == v:
                    f = True
                    break
            if not f:
                found = False
                break
        if found:
            return dic
    return None

def createXMLStructureForFiles(el, fileInfo, namespace='mets'):
    empty = True
    t = xmlElement(el.tag, namespace)
    if el.text is not None:
        text = el.text.replace('\n', '').replace(' ', '')
        if text != '':
            if text in fileInfo:
                empty = False
                t.value = fileInfo[el.text]
    for child in el:
        if child.tag == 'attr':
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

templatename = 'template.xml'
pars = etree.parse(templatename)
rootEl = createXMLStructure(pars.getroot(), info)
if len(files) < 1:
    files.append(os.open(info['filename'],os.O_RDWR|os.O_CREAT))
if rootEl.printXML(files[0]):
    parseFiles('/SIP/huge/corp')
    rootEl.printXML(files[0])
    #add file to bottom of xml
    f = files[0]
    for filename in filenames:
        # add tmp file to end of xml
        fd = os.open(filename, os.O_RDONLY)
        while True:
            data = os.read(fd, 65536)
            if data:
                os.write(f, data)
            else:
                break
        # print more XML
        rootEl.printXML(files[0])
