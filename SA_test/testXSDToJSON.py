
from lxml import etree
import os
import json

complexTypes = {}
attributeGroups = {}
pretty = True
eol_ = '\n'

def getIndent(level):
    indent = ''
    for i in range(level):
        indent += '   '
    return indent

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

class xmlElement():

    def __init__(self, name):
        self.name = name
        self.children = []
        # self.tagName = tagName
        # self.children = []
        self.attributes = []
        self.attrib = []
        self.value = ''
        self.karMin = 0
        self.karMax = -1
        # self.namespace = namespace
        # self.completeTagName = ''
        # self.containsFiles = False
        # self.printed = 0
        # if self.namespace != '':
            # self.completeTagName += self.namespace + ':'
        # self.completeTagName += str(self.tagName)

    def printXML(self, fd, level=0):
        # if self.containsFiles:
            # print "contaions iles: " + self.tagName
        pretty_print(fd, level, pretty)
        os.write(fd, '<' + self.name)
        for a in self.attributes:
            a.printXML(fd)
        if self.children or self.value is not '':
            os.write(fd, '>' + eol_)
            for child in self.children:
                if child.printXML(fd, level + 1):
                    return True
            if self.value is not '':
                pretty_print(fd, level + 1, pretty)
                os.write(fd, self.value + eol_)
            pretty_print(fd, level, pretty)
            os.write(fd, '</' + self.name + '>' + eol_)
        else:
            os.write(fd, '/>' + eol_)

        # for att in self.attrib:
            # print self.name + ': ' + att + ': ' + str(self.attrib[att])

    def generateJSON(self):
        result = {}
        result['name'] = self.name
        children = []
        for child in self.children:
            children.append(child.generateJSON())
        result['children'] = children
        result['attributes'] = self.attrib
        return result

    def isEmpty(self):
        if self.value != '' or self.children:
            return False
        else:
            return True

    def addChild(self, child):
        # print 'child: ' + child
        self.children.append(child)

    def printDebug(self, level = 0):
        print getIndent(level) + self.name
        for child in self.children:
            child.printDebug(level+1)

def printTag(tag):
    if isinstance(tag, str):
        a = tag.split('}')
        if len(a) > 1:
            return a[1]
        else:
            return tag
    else:
        return 'unknown tag: ' + str(type(tag))

def getPrefix(tag):
    if tag is None:
        return None
    tag = tag.split(':')
    if len(tag) > 0:
        return tag[0]
    else:
        return ''

def getPostfix(tag):
    if tag is None:
        return None
    tag = tag.split(':')
    if len(tag) > 1:
        return tag[1]
    else:
        return ''

def analyze2(element, tree=None, usedTypes=[]):
    # print element.local-name()
    tag = printTag(element.tag)
    # print tag
    if tag == 'element':
        if element.get('type') is None:
            t = xmlElement(element.get('name'))
            tree.addChild(t)
            for child in element:
                analyze2(child, t, usedTypes)
        elif getPrefix(element.get('type')) == 'xsd':
            t = xmlElement(element.get('name'))
            tree.addChild(t)
        else:
            t = xmlElement(element.get('name'))
            tree.addChild(t)
            key = element.get('type')
            if key not in usedTypes:
                if key in complexTypes:
                    usedTypes.append(key)
                    for child in complexTypes[key]:
                        analyze2(child, t, usedTypes)
                else:
                    print "type unknown: " + element.get('type')
    elif tag == 'complexType':
        for child in element:
            analyze2(child, tree, usedTypes)
    elif tag == 'complexContent':
        for child in element:
            analyze2(child, tree, usedTypes)
    elif tag == 'extension':
        if element.get('base'):
            t = element.get('base')
            # print t
            if t not in usedTypes:
                if t in complexTypes:
                    usedTypes.append(t)
                    for child in complexTypes[t]:
                        analyze2(child, tree, usedTypes)
    elif tag == 'sequence':
        for child in element:
            analyze2(child, tree, usedTypes)
    elif tag == 'choice':
        for child in element:
            analyze2(child, tree, usedTypes)
    elif tag == 'attribute':
        if element.get('type') is not None:
            att = {}
            att['type'] = 'input'
            att['key'] = element.get('name')
            templateOptions = {}
            templateOptions['type'] = 'text'  #TODO add options
            templateOptions['label'] = element.get('name')
            att['templateOptions'] = templateOptions
            # templateOptions['placeholder'] = 'text'
            # templateOptions['required'] #TODO
            # att['type'] = element.get('type')
            # att['use'] = element.get('use')
            # tree.attrib[element.get('name')] = att
            tree.attrib.append(att)
            # print att
        else:
            if element.get('name') is not None:
                att = {}
                att['key'] = element.get('name')
                # att['use'] = element.get('use')
                templateOptions = {}
                templateOptions['label'] = element.get('name')
                for child in element:
                    if printTag(child.tag) == 'simpleType':
                        restrictions = {}
                        for ch in child:
                            if printTag(ch.tag) == 'restriction':
                                enumerations = []
                                for c in ch:
                                    if printTag(c.tag) == 'enumeration':
                                        att['type'] = 'select'
                                        a = {}
                                        a['name'] = c.get('value')
                                        a['value'] = c.get('value')
                                        enumerations.append(a)
                                    else:
                                        if isinstance(c.tag, str):
                                            print "unknown restriction: " + c.tag
                                        pass
                                if len(enumerations) > 0:
                                    templateOptions['options'] = enumerations
                        # print restrictions
                # print att
                att['templateOptions'] = templateOptions
                tree.attrib.append(att)
                # tree.attrib[element.get('name')] = att
            else:
                print "ERROR: attribute name is none"

    elif tag == 'attributeGroup':
        if element.get('ref'):
            ref = element.get('ref')
            if ref in attributeGroups:
                for child in attributeGroups[ref]:
                    analyze2(child, tree, usedTypes)
        pass
    else:
        print 'other: ' + tag

## TODO list:

# 1. text content of elements

# 2. required or not (All other information)

# 3. save the model to a jsonTemplate (might prioritate this)


# pars = etree.parse("testSchema.xsd")
pars = etree.parse("CSPackageMETS.xsd")
# rootEl = create2(pars.getroot())

schema = '{http://www.w3.org/2001/XMLSchema}'

root = pars.getroot()

# print root.tag
# analyze(root)

def changeName(tree):
    tree.name = 'test'

for child in root.iterfind(schema + 'complexType'):
    if child.get('name'):
        complexTypes[child.get('name')] = child

for child in root.iterfind(schema + 'attributeGroup'):
    if child.get('name'):
        attributeGroups[child.get('name')] = child

t = None

xmlFile = os.open('test.txt',os.O_RDWR|os.O_CREAT)

el = xmlElement('not test')

for child in root.iterfind(schema + 'element'):
    tag = printTag(child.tag)
    if tag != 'complexType' and tag != 'attributeGroup':
        tree = xmlElement(child.get('name'))
        for ch in child:
            analyze2(ch, tree)
        if tree is not None:
            with open('test.txt', 'wb') as outfile:
                json.dump(tree.generateJSON(), outfile)
            # tree.printDebug()
            # tree.printXML(xmlFile)
            # print tree.generateJSON()
        # ch = analyze(child)
        # if ch != None:
        #     for c in ch:
        #         c.printXML(xmlFile)
#     for c in child:
#         if printTag(child.tag) == 'complexType':
#             # go deeper
#             for ch in c:
#
#     print printTag(child.tag)

# attribute = {
#     "MIMETYPE": {
#         "type": "string",
#         "use": "optional"
#     },
#     "CHECKSUMTYPE": {
#         "type": "string",
#         "use":"optional",
#         "restrictions": {
#             "enumeration": ["MD5", "SHA-1", "SHA-256"]
#         }
#     }
# }
#
# attribute2 = [
#     {
#         'key': 'ROLE',
#         'type': 'input',
#         'templateOptions': {
#             'type': 'text',
#             'label': 'ROLE',
#             'placeholder': 'string',
#             'required': True
#         }
#     },
#     {
#         'key': 'OTHERROLE',
#         'type': 'select',
#         'templateOptions': {
#             'label': 'OTHERROLE',
#             'options': [
#                 {'name': 'CREATOR', 'value': 'CREATOR'},
#                 {'name': 'EDITOR', 'value': 'EDITOR'},
#                 {'name': 'ARCHIVIST', 'value': 'ARCHIVIST'},
#             ]
#         }
#     },
# ]

# result = {
#     {
#         "name": "mets",
#         "children": [
#             #repeat
#         ],
#         "attributes": [
#             {
#                 'key': 'ROLE',
#                 'type': 'input',
#                 'templateOptions': {
#                     'type': 'text',
#                     'label': 'ROLE',
#                     'placeholder': 'string',
#                     'required': 'True'
#                 }
#             },
#             {
#                 'key': 'OTHERROLE',
#                 'type': 'select',
#                 'templateOptions': {
#                     'label': 'OTHERROLE',
#                     'options': [
#                         {'name': 'CREATOR', 'value': 'CREATOR'},
#                         {'name': 'EDITOR', 'value': 'EDITOR'},
#                         {'name': 'ARCHIVIST', 'value': 'ARCHIVIST'},
#                     ]
#                 }
#             }
#         ],
#         "meta": {
#             "min": "0",
#             "max": "1"
#         }
#     }
# }
