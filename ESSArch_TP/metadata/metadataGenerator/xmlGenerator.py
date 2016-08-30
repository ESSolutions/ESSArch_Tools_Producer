import os, re
import hashlib
import uuid
import json
import copy
from collections import OrderedDict
import fileinput

from xmlStructure import xmlElement, xmlAttribute, fileInfo, fileObject, dlog

sortedFiles = []
foundFiles = 0

def calculateChecksum(filename):
    """
    calculate the checksum for the selected file, one chunk at a time
    """
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
    """
    walk through the choosen folder and parse all the files to their own temporary location
    """
    fileInfo = {}

    for dirname, dirnames, filenames in os.walk(filename):
        # print dirname
        for file in filenames:

            # populate dictionary

            fileInfo['FName'] = dirname+'/'+file
            fileInfo['FChecksum'] = calculateChecksum(dirname+'/'+file)
            fileInfo['FID'] = uuid.uuid4().__str__()
            fileInfo['FMimetype'] = 'application/x-tar'
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
    """
    remove excess of whitespaces and check if the key exists in the dictionary
    """
    if key is not None:
        text = key.rstrip()
        if text != '':
            # print tree.text.replace('\n', '').replace(' ','')
            if text in info:
                return info[text]
    return None

def parseChild(name, content, info, namespace, t, fob, level=0):
    """
    Parse a child to get the correct values even if the values are in an array
    """
    if '-arr' not in content:
        c = createXMLStructure(name, content, info, fob, namespace, level+1)
        if c is not None:
            t.addChild(c)
    else:
        occurrences = 1
        if '-max' in content:
            occurrences = content['-max']
            if occurrences == -1:
                occurrences = 10000000000 # unlikely to surpass this
        #parse array string and pass info
        arguments = content['-arr']
        testArgs = arguments['arguments']
        dictionaries = copy.deepcopy(info[arguments['arrayName']])
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
    """
    The main XML element creator where the json structure is broken down and converted into a xml.
    """
    global foundFiles
    t = xmlElement(name, namespace)
    # loop through all attribute and children
    if '-containsFiles' in content and fob is not None:
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
            foundFiles += 1

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
                        if attrib['-req'] == 1:
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
            if isinstance(value, OrderedDict) or isinstance(value, dict):
                parseChild(key, value, info, namespace, t, fob, level)
            elif isinstance(value, list):
                for l in value:
                    parseChild(key, l, info, namespace, t, fob, level)

    if t.isEmpty():
        if  '-allowEmpty' in content:
            if content['-allowEmpty'] != 1:
                return None
            else:
                return t
        else:
            return None
    else:
        return t

def findMatchingSubDict(dictionaries, arguments):
    """
    test if all the arguments are present and correct in the selected dictionary
    """
    for dic in dictionaries:
        # compare agent dicts
        found = True
        for key, value in arguments.iteritems():
            if key in dic:
                if dic[key] != value:
                    found = False
            else:
                found = False
        if found:
            return dic
    return None

def parseAttribute(content, info):
    """
    parse the content of an attribute and return it
    """
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

def createXML(info, filesToCreate, folderToParse):
    """
    The task method for executing the xmlGenerator and completing the xml files
    This is also the TASK to be run in the background.
    """

    global sortedFiles
    global foundFiles

    sortedFiles = []
    foundFiles = 0

    for key, value in filesToCreate.iteritems():
        json_data=open(value).read()
        try:
            data = json.loads(json_data, object_pairs_hook=OrderedDict)
        except ValueError as err:
            print err # implement logger
            return  False
        name, rootE = data.items()[0] # root element
        xmlFile = os.open(key,os.O_RDWR|os.O_CREAT)
        fob = fileObject(key, value, xmlFile)
        sortedFiles.append(fob)
        rootEl = createXMLStructure(name, rootE, info, fob)
        rootEl.printXML(xmlFile)
        fob.rootElement = rootEl

    parseFiles(folderToParse)

    # add the tmp files to the bottom of the appropriate file and write out the next section of xml until it's done
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


def appendXML(inputData):
    """
    Searches throught the file for the expected tag and appends the new element before the end (appending it to the end)
    """
    for line in fileinput.FileInput(inputData['path'],inplace=1):
        if "</"+inputData['elementToAppendTo']+">" in line:
            name, rootE = inputData['template'].items()[0]
            rootEl = createXMLStructure(name, rootE, inputData['data'])
            level = (len(line) - len(line.lstrip(' ')))/4
            rootEl.XMLToString(level+1)
        print line,
