"""sdf."""
# import os
import sys
from lxml import etree


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


############## ((  TODO  )) ##############

# 1. sanitize all attributes and values

# 2. indentation for pretty print

# 3. namespace


# info = {"UUID": "aslfd24lkn2l34nl2", "AgentType": "ORGANIZATION"}
info = {"xmlns:mets":"http://www.loc.gov/METS/",
        "xmlns:ext":"ExtensionMETS",
        "xmlns:xlink":"http://www.w3.org/1999/xlink",
        "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation":"http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd",
        "PROFILE":"http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xmll",
        "LABEL":"Test of SIP 1",
        "TYPE":"Personnel",
        # "mets:ID":"ID8b42fed2-c281-43b4-9798-5168126b0a4b",
        "OBJID":"UUID:9bc10faa-3fff-4a8f-bf9a-638841061065",
        "ext:CONTENTTYPESPECIFICATION":"FGS Personal, version 1",
        "CREATEDATE":"2016-06-08T10:44:00+02:00",
        "RECORDSTATUS":"NEW",
        "ext:OAISTYPE":"SIP",
        "agentName":"name",
        "agentNote":"note",
       }

# xmlFile = """
# <mets min="1" max="1">
#     <attr name="xmlns:mets" req="1">xmlns:mets</attr>
#     <attr name="xmlns:ext" req="1">xmlns:ext</attr>
#     <attr name="xmlns:xlink" req="1">xmlns:xlink</attr>
#     <attr name="xmlns:xsi" req="1">xmlns:xsi</attr>
#     <attr name="xsi:schemaLocation" req="1">xsi:schemaLocation</attr>
#     <attr name="PROFILE" req="1">mets:PROFILE</attr>
#     <attr name="LABEL" req="0" allowed="1">mets:LABEL</attr>
#     <attr name="TYPE" req="1">mets:TYPE</attr>
#     <attr name="OBJID" req="1">mets:OBJID</attr>
#     <attr name="ext:CONTENTTYPESPECIFICATION" req="0" allowed="1">ext:CONTENTTYPESPECIFICATION</attr>
#     <attr name="ext:SYSTEMTYPE" req="0" allowed="1">ext:SYSTEMTYPE</attr>
#     <attr name="ext:DATASUBMISSIONSESSION" req="0" allowed="1">ext:DATASUBMISSIONSESSION</attr>
#     <attr name="ext:PACKAGENUMBER" req="0" allowed="1">ext:PACKAGENUMBER</attr>
#     <attr name="ext:ARCHIVALNAME" req="0" allowed="1">ext:ARCHIVALNAME</attr>
#     <attr name="ext:APPRAISAL" req="0" allowed="1">ext:APPRAISAL</attr>
#     <attr name="ext:ACCESSRESTRICT" req="0" allowed="1">ext:ACCESSRESTRICT</attr>
#     <attr name="ext::STARTDATE" req="0" allowed="1">ext:STARTDATE</attr>
#     <attr name="ext:ENDDATE" req="0" allowed="1">ext:ENDDATE</attr>
#     <attr name="ext::INFORMATIONCLASS" req="0" allowed="1">ext:INFORMATIONCLASS</attr>
#     <metsHdr min="0" max="1">UUID</metsHdr>
# </mets>
# """

eol_ = '\n'

debug = False
pretty = True

def dlog(string):
    if debug:
        print string

def pretty_print(level, pretty):
    if pretty:
        for idx in range(level):
            sys.stdout.write('    ')


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

    def printXML(self):
        if self.value is not '':
            sys.stdout.write(' ' + self.attrName + '="' + self.value + '"')


class xmlElement(object):
    '''
    dsf.
    '''

    def __init__(self, tagName='', namespace = ''):
        self.tagName = tagName
        self.children = []
        self.attributes = []
        self.value = ''
        self.karMin = 0
        self.karMax = -1
        self.namespace = namespace
        self.completeTagName = ''
        if self.namespace != '':
            self.completeTagName += self.namespace + ':'
        self.completeTagName += str(self.tagName)

    def setNamespace(self, namespace):
        self.namespace = namespace
        self.completeTagName = ''
        if self.namespace != '':
            self.completeTagName += self.namespace + ':'
        self.completeTagName += self.tagName

    def printXML(self, level=0):
        pretty_print(level, pretty)
        sys.stdout.write('<' + self.completeTagName)
        for a in self.attributes:
            a.printXML()
        if self.children or self.value is not '':
            sys.stdout.write('>' + eol_)
            for child in self.children:
                child.printXML(level+1)
            if self.value is not '':
                pretty_print(level+1, pretty)
                sys.stdout.write(self.value + eol_)
            pretty_print(level, pretty)
            sys.stdout.write('</' + self.completeTagName + '>' + eol_)
        else:
            sys.stdout.write('/>' + eol_)

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

    def addChild(self, el):
        if el.namespace == '':
            el.setNamespace(self.namespace)
        self.children.append(el)

def create2(tree, namespace = ''):
    empty = True
    hasAttrib = False
    t = xmlElement(tree.tag, namespace)
    if tree.text is not None:
        if tree.text in info:
            empty = False
            t.value = info[tree.text]
    for child in tree:
        if child.tag == 'attr':
            # value = info[child.text]
            if child.get('value') is '1':
                hasAttrib = True
                t.addAttribute(xmlAttribute(child.get('name'), child.text))
            else:
                if child.text in info:
                    hasAttrib = True
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

# parser = etree.XMLParser(remove_blank_text=True)
# pars = etree.XML(xmlFile, parser)

pars = etree.parse("SA_test/template.xml")

rootEl = create2(pars.getroot())
rootEl.printXML()

# print etree.tostring(root)

# e = xmlElement('mets')
# b = xmlElement('agent')
# e.addAttribute(xmlAttribute('ID', '2k3lno42'))
# e.addChild(b)
# e.printXML()
