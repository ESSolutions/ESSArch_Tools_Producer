from lxml import etree
import os
import hashlib
import time
import uuid

from jobtastic import JobtasticTask

class LotsOfDivisionTask(JobtasticTask):
    """
    Division is hard. Make Celery do it a bunch.
    """
    # These are the Task kwargs that matter for caching purposes
    significant_kwargs = [
        ('numerators', str),
        ('denominators', str),
    ]
    # How long should we give a task before assuming it has failed?
    herd_avoidance_timeout = 10  # Shouldn't take more than 60 seconds
    # How long we want to cache results with identical ``significant_kwargs``
    cache_duration = 0  # Cache these results forever. Math is pretty stable.
    # Note: 0 means different things in different cache backends. RTFM for yours.

    def calculate_result(self, numerators, denominators, **kwargs):
        """
        MATH!!!
        """
        results = []
        divisions_to_do = len(numerators)
        # Only actually update the progress in the backend every 10 operations
        update_frequency = 10
        for count, divisors in enumerate(zip(numerators, denominators)):
            numerator, denominator = divisors
            results.append(numerator / denominator)
            # Let's let everyone know how we're doing
            self.update_progress(
                count,
                divisions_to_do,
                update_frequency=update_frequency,
            )
            # Let's pretend that we're using the computers that landed us on the moon
            # sleep(0.1)

        return results


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

def parseFiles(filename='/SIP/huge', level=3):
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
                c = createXMLStructure(child, namespace)
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

class xmlGenerator(JobtasticTask):

    info = {}
    templatename = ''

    def calculate_result(self, info, templatename):
        pars = etree.parse(self.templatename)
        rootEl = createXMLStructure(pars.getroot(), self.info)
        if len(files) < 1:
            files.append(os.open(self.info['filename'],os.O_RDWR|os.O_CREAT))
        if rootEl.printXML(files[0]):
            parseFiles()
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
