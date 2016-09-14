# import os
import json
from collections import OrderedDict

# oppna json# ga igenom,
# element for element och kolla om alla elementen ar ok

def checkElement(element):
    otherExists = False
    for key, value in element.iteritems():
        if key[:1] == '-':
            if key == '-attr':
                if not isinstance(value, list):
                    print "ERROR: '-attr' does not contain a list in element: " + key
                else:
                    for attr in value:
                        checkAttribute(attr)
            elif key == '-min':
                if isinstance(value, int):
                    if value < 0:
                        print "ERROR: '-min' value cannot be smaler than 0"
                    else:
                        if otherExists:
                            if value > element['-max']:
                                print "ERROR: '-min' ("+str(value)+") cannot be greater than '-max'("+str(element['-max'])+")"
                else:
                    print "ERROR: '-min' attribute can only contain a int not: " + type(value)
                otherExists = True
            elif key == '-max':
                if isinstance(value, int):
                    if value < -1 or value == 0:
                        print "ERROR: '-max' value cannot be smaler than 0 exept for -1 (infinite number)"
                    else:
                        if otherExists:
                            if value < element['-min']:
                                print "ERROR: '-max' ("+str(value)+") cannot be smaller than '-min'("+str(element['-min'])+")"
                else:
                    print "ERROR: '-max' attribute can only contain a int not: " + str(type(value))
                otherExists = True
            elif key == '-allowEmpty':
                if isinstance(value, int):
                    if value != 1:
                        if value == 0:
                            print "INFO: '-allowEmpty' could be removed since it is not required with value 0"
                        else:
                            print "ERROR: '-allowEmpty' can not have values other than 1 and 0"
                else:
                    print "ERROR: '-allowEmpty' attribute can only contain a int not: " + str(type(value))
            elif key == '-namespace':
                if not isinstance(value, unicode):
                    print "ERROR: '-namespace' attribute can only contain a string not: " + str(type(value))
            elif key == '-arr':
                if isinstance(value, OrderedDict):
                    checkArguments(value)
                else:
                    print "ERROR: '-arr' attribute can only contain an OrderedDict not: " + str(type(value))
            elif key == '-containsFiles':
                pass
            else:
                print "ERROR: unknown attribute: '" + key + "'"
        elif key[:1] == '#':
            checkContentElement(value)
        else:
            if isinstance(value, OrderedDict):
                checkElement(value)
            elif isinstance(value, list):
                for el in value:
                    if isinstance(el, OrderedDict):
                        checkElement(el)
                    else:
                        print "ERROR: '-arr' attribute can only contain a OrderedDict not: " + str(type(value))

def checkArguments(element):
    for key, value in element.iteritems():
        if key == 'arrayName':
            if not isinstance(value, unicode):
                print "ERROR: 'arrayName' attribute can only contain a string not: " + str(type(value))
        elif key == 'arguments':
            if isinstance(value, OrderedDict):
                for k, v in value.iteritems():
                    if not isinstance(v, unicode):
                        print "ERROR: 'arguments' attribute can only contain a string not: " + str(type(v))
            else:
                print "ERROR: 'arguments' attribute can only contain a string not: " + str(type(value))
        else:
            print "ERROR: unknown element: '" + key + "'"
        pass

def checkAttribute(element):
    foundName = False
    if not isinstance(element, OrderedDict):
        print "ERROR: '-attr' attributes is not an dictionary. should be something like '-attr': [{'-name':'attributename'}]"
        return
    for key, value in element.iteritems():
        if key == '-name':
            foundName = True
        elif key == '#content':
            checkContentElement(value)
        elif key == '-req':
            if isinstance(value, int):
                if value == 0:
                    print "INFO: '-req' could be removed since it is not required with value 0"
                elif value != 1:
                    print "ERROR: '-req' for attribute can't be greater than 1"
            else:
                print "ERROR: value of '-req' can only be int not " + str(type(value))
        else:
            print "ERROR: unknown attribute: '" + key + "'"

    if not foundName:
        print "ERROR: '-name' missing in attribute: " # TODO attribute name

def checkContentElement(element):

    if isinstance(element, list):
        for el in element:
            for key, value in el.iteritems():
                if key == 'text':
                    if not isinstance(key, unicode):
                        print "ERROR: '#content' key 'text' does not contain a string"
                elif key == 'var':
                    if not isinstance(key, unicode):
                        print "ERROR: '#content' key 'var' does not contain a string"
                        # TODO in some future this could include a check if the variable exists
                else:
                    print "ERROR: unknown key '" + key + "' in '#content'"
    else:
        print "ERROR: '#content' attribute should always contain a list"

    pass




jsonfile = 'templates/JSONTemplate.json'
json_data=open(jsonfile).read()
try:
    data = json.loads(json_data, object_pairs_hook=OrderedDict)
except ValueError as err:
    print err # implement logger

checkElement(data)
