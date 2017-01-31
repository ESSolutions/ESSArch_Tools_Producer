#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
'''
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2013  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
'''

from lxml import etree
import os, pytz, datetime, stat, hashlib

# own models etc
#xx 


"An example of fast parse iteration of a file"
###############################################
#context = etree.iterparse( MYFILE, tag='item' )
#fast_iter(context,process_element)
def fast_iter(context, func):    
        
    for event, elem in context:
        func(elem) 
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


"Function for fast parse iteration"
###############################################    
def process_element(elem):
     
    print elem.tag
    #print elem.xpath('description/text()')    
    #context = etree.iterparse( sourcefile )
    #for event, element in context:
    #    if element.tag == 'mets' and element.tag == 'ID':
    #        IPUUID = element.tag
    #        if exit_condition: break


"Checksum calculations"
###############################################
def calcsum(filepath,checksumtype='md5'):
    """Return checksum for a file."""
    checksumtype = checksumtype.lower()
    if checksumtype == 'md5':
        h = hashlib.md5()
    elif checksumtype == 'sha-256':
        h = hashlib.sha256()
    else:
        h = hashlib.md5()
    f = open(filepath, "rb")
    s = f.read(1048576)
    while s != "":
        h.update(s)
        s = f.read(1048576)
    f.close()
    return h.hexdigest()


"Create a time stamp"
###############################################
def creation_time(time_zone):
    # create timestamp
    #stockholm=pytz.timezone('Europe/Stockholm') 
    stockholm=pytz.timezone(time_zone)
    dt = datetime.datetime.utcnow().replace(microsecond=0,tzinfo=pytz.utc)    
    loc_dt_isoformat = dt.astimezone(stockholm).isoformat()
    creation_time = loc_dt_isoformat
 
    return creation_time


"Remove element from memory"
###############################################
def clearNode(elem):
    # remove element from memory
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]


"Parse namespaces from XML file"
###############################################
def ParseNSXMLFile(filename):
    # parse namespaces in xml file

    events = ('start-ns', 'end-ns')
    namespaces = []
    
    context = etree.iterparse( filename, events=events)
        
    # get namespaces
    for event, elem in context:
        if event == "start-ns":
            namespaces.insert(0, elem)
            #if namespaces[0][0] == 'mets' : mets_ns = '{%s}' %namespaces[0][1]
            #print namespaces[0]
    return namespaces

    
"Parse XML file"
###############################################
def ParseXMLFile(filename):
    # parse xml file > 2 GB e.q high performance
   
    # find out which xml type based on namespace
    namespaces = ParseNSXMLFile(filename)
    for n in namespaces :
        if n[0] == 'mets' :
            ns = 'mets'
    
    # if xml type is mets
    if ns == 'mets' :
        
        # tags to check for in root of xml file
        tags_root = [ 'LABEL', 'OBJID','PROFILE', 'TYPE', 'ID' ]
        
        # only parse start and end elements
        events = ('start', 'end', )
        
        # declare variables
        root = None
        metadata = [] 
        m_root = [] 
        m_metshdr = [] 
        m_agent = []
        m_altrecordid = []
        
        # iterparse xml file
        context = etree.iterparse( filename, events=events)
    
        # get metadata in xml file
        for event, elem in context:
            
            ##########################################        
            # separate namespace from tag
            namespace, tag = elem.tag[1:].split('}', 1)
            
            ##########################################
            # get root elements metadata
            if event == 'start' and root is None:
                root = elem.tag
                for tr in tags_root:
                    m_root.append(elem.get(tr))
                clearNode(elem)
                
            ##########################################
            # get metsHdr element metadata
            if event == 'start' and tag == 'metsHdr' :
                m_metshdr.append(elem.get('CREATEDATE'))
                m_metshdr.append(elem.get('RECORDSTATUS'))
                clearNode(elem)
                
            ##########################################
            # get metsDocumentID element metadata
            if event == 'end' and tag == 'metsDocumentID' :
                m_metshdr.append(elem.text)
                clearNode(elem)
                    
            ##########################################
            # get agent elements metadata
            if event == 'end' and tag == 'agent' :
                cnt = 1
                m_NOTE = []
                m_ROLE = elem.get('ROLE')
                m_TYPE = elem.get('TYPE')
                m_OTHERTYPE = elem.get('OTHERTYPE')
                m_NAME = elem[0].text
                try :
                    while (len(elem[cnt].text)) :
                        m_NOTE.append(elem[cnt].text)
                        cnt +=1
                except IndexError:
                    pass
                m_agent.append([m_ROLE,m_TYPE,m_OTHERTYPE, m_NAME, m_NOTE])
                clearNode(elem)
                
            ##########################################
            # get altrecordid elements metadata
            if event == 'end' and tag == 'altRecordID' :
                m_TYPE = elem.get('TYPE')
                m_TEXT = elem.text
                m_altrecordid.append([m_TYPE, m_TEXT])
                clearNode(elem)
            
        # concatenate all the results    
        metadata.append(m_root)
        metadata.append(m_metshdr)
        metadata.append(m_agent)
        metadata.append(m_altrecordid)
    
        # remove context from memory
        del context

    else:
        print "Not a METS file"

    return metadata


"Get filetree"
###############################################
def GetFiletree(path='/ESSArch/testdata/A0007601'):
    file_list = []
    for f in os.listdir(path):
        path = os.path.join(path,f) 
        mode = os.stat(path)
        if stat.S_ISREG(mode[0]):                   # It's a file
            file_list.append(f)
        elif stat.S_ISDIR(mode[0]):                 # It's a directory
            for df in GetFiletree(path):
                file_list.append(f + '/' + df)
    return file_list


"Convert string to unicode"
###############################################
def str2unicode(x,y=None):
    if type(x).__name__ == 'str':
        try:
            res = x.decode('utf-8')
        except UnicodeDecodeError:
            res = x.decode('iso-8859-1')
    elif type(x).__name__ == 'list':
        num = 0
        for i in x:
            x[num] = str2unicode(i)
            num += 1
        res = x
    elif type(x).__name__ == 'int' or type(x).__name__ == 'long':
        res = str2unicode(str(x))
    elif type(x).__name__ == 'NoneType' and not type(y).__name__ == 'NoneType':
        res = str2unicode(y)
    else:
        res = x
    return res

