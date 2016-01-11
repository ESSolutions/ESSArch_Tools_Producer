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

from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django import forms

import sys, datetime


#class ControlAreaForm_file():
#    #ObjectIdentifierValue = forms.CharField(label='ObjectIdentifierValue',required=False, widget = forms.HiddenInput())
#    FileSelect_CHOICES = ()
#    filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.CheckboxSelectMultiple())
#    def __init__(self, *args, **kwargs):
#        super(ControlAreaForm_file, self ).__init__(*args, **kwargs)
#        if self.FileSelect_CHOICES:
#            self.fields['filename'].choices = self.FileSelect_CHOICES

#Choices_FileSelect = ()

Choices_DeliveryType = (
    ('ERMS','ERMS'),
    ('Personnel','Personnel'),
    ('Journals','Journals'),
    ('Economics','Economics'),
    ('Databases','Databases'),
    ('Webpages','Webpages'),
    ('GIS','GIS'),
    ('No specification','No specification'),
    ('AIC','AIC'),
    ('Publication','Publication'),
    ('Deposit','Deposit'),
    ('Agreement','Agreement'),
)


class PlainText(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        if not value=='' and hasattr(self, 'choices'):
            value_label = dict(self.choices)[value]
        else:
            value_label = value
        return mark_safe(u'<input type="hidden" name="%s" %s value="%s" />%s' % (name,flatatt(final_attrs),value,value_label))


# Logevents
class LogEvent(models.Model):
    eventType   = models.IntegerField( default=0, unique=True )
    eventDetail = models.CharField( max_length = 255 )

    class Meta:
        ordering = ['eventType']
        permissions = (
                       ("Can_view_log_menu", "Can_view_log_menu"),
                       )
	verbose_name = 'Log Event'

    def __unicode__(self):
        # create a unicode representation of this object
        return self.eventDetail

    def populate_from_form(self, form):
        # pull out all fields from a form and use them to set
        # the values of this object.
        for field in LogEvent._meta.fields:
            if field.name in form.cleaned_data:
                setattr( self, field.name, form.cleaned_data[field.name] )

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self) 
                 for field in LogEvent._meta.fields }


# Parameters
class Parameter(models.Model):
    entity      = models.CharField( max_length = 60, unique=True )
    value       = models.CharField( max_length = 70 )
    
    class Meta:
        ordering = ["entity"]

    def __unicode__(self):
        # create a unicode representation of this object
        return self.entity
    
    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self) 
                 for field in Parameter._meta.fields }


# Paths
class Path(models.Model):
    entity  = models.CharField( max_length = 60, unique=True )
    value   = models.CharField( max_length = 70 )

    class Meta:
        ordering = ["entity"]

 
# XML schemas and namespaces
class SchemaProfile(models.Model):
    entity      = models.CharField( max_length = 60, unique=True )
    value       = models.CharField( max_length = 70 )
    
    class Meta:
        ordering = ["entity"]
   	verbose_name = 'XML Schema' 

# General metadata for information package
# Additional metadata for information package
# Reference metadata for files in information package
class IPParameter(models.Model):
    objid                                           = models.CharField( max_length = 255, unique=True   ) # General metadata for information package
    label                                           = models.CharField( max_length = 255 )
    type                                            = models.CharField( max_length = 255 )
    createdate                                      = models.CharField( max_length = 255 )
    recordstatus                                    = models.CharField( max_length = 255 )
    deliverytype                                    = models.CharField( max_length = 255 )
    deliveryspecification                           = models.CharField( max_length = 255 )
    submissionagreement                             = models.CharField( max_length = 255 )
    systemtype                                      = models.CharField( max_length = 255 )
    previoussubmissionagreement                     = models.CharField( max_length = 255 )
    datasubmissionsession                           = models.CharField( max_length = 255 )
    packagenumber                                   = models.CharField( max_length = 255 )
    referencecode                                   = models.CharField( max_length = 255 )
    previousreferencecode                           = models.CharField( max_length = 255 )
    appraisal                                       = models.CharField( max_length = 255 )
    accessrestrict                                  = models.CharField( max_length = 255 )
    startdate                                       = models.CharField( max_length = 255 )
    enddate                                         = models.CharField( max_length = 255 )
    informationclass                                = models.CharField( max_length = 255 )
    archivist_organization                          = models.CharField( max_length = 255 )
    archivist_organization_id                       = models.CharField( max_length = 255 )
    archivist_organization_software                 = models.CharField( max_length = 255 )
    archivist_organization_software_id              = models.CharField( max_length = 255 )
    archivist_organization_software_type            = models.CharField( max_length = 255 )
    archivist_organization_software_type_version    = models.CharField( max_length = 255 )
    archivist_individual                            = models.CharField( max_length = 255 )
    archivist_individual_telephone                  = models.CharField( max_length = 255 )
    archivist_individual_email                      = models.CharField( max_length = 255 )
    creator_organization                            = models.CharField( max_length = 255 )
    creator_organization_id                         = models.CharField( max_length = 255 )
    creator_individual                              = models.CharField( max_length = 255 )
    creator_individual_details                      = models.CharField( max_length = 255 )
    creator_individual_telephone                    = models.CharField( max_length = 255 )
    creator_individual_email                        = models.CharField( max_length = 255 )
    creator_software                                = models.CharField( max_length = 255 )
    creator_software_id                             = models.CharField( max_length = 255 )
    producer_organization                           = models.CharField( max_length = 255 )
    producer_organization_id                        = models.CharField( max_length = 255 )
    producer_individual                             = models.CharField( max_length = 255 )
    producer_individual_telephone                   = models.CharField( max_length = 255 )
    producer_individual_email                       = models.CharField( max_length = 255 )
    producer_organization_software                  = models.CharField( max_length = 255 )
    producer_organization_software_identity         = models.CharField( max_length = 255 )
    producer_organization_software_type             = models.CharField( max_length = 255 )
    producer_organization_software_type_version     = models.CharField( max_length = 255 )
    submitter_organization                          = models.CharField( max_length = 255 )
    submitter_organization_id                       = models.CharField( max_length = 255 )
    submitter_individual                            = models.CharField( max_length = 255 )
    submitter_individual_telephone                  = models.CharField( max_length = 255 )
    submitter_individual_email                      = models.CharField( max_length = 255 )
    ipowner_organization                            = models.CharField( max_length = 255 )
    ipowner_organization_id                         = models.CharField( max_length = 255 )
    ipowner_individual                              = models.CharField( max_length = 255 )
    ipowner_individual_telephone                    = models.CharField( max_length = 255 )
    ipowner_individual_email                        = models.CharField( max_length = 255 )
    editor_organization                             = models.CharField( max_length = 255 )
    editor_organization_id                          = models.CharField( max_length = 255 )
    preservation_organization                       = models.CharField( max_length = 255 )
    preservation_organization_id                    = models.CharField( max_length = 255 )
    preservation_organization_software              = models.CharField( max_length = 255 )
    preservation_organization_software_id           = models.CharField( max_length = 255 )
    file_id                                         = models.CharField( max_length = 255 ) # Reference metadata for files in information package
    file_name                                       = models.CharField( max_length = 255 )
    file_createdate                                 = models.CharField( max_length = 255 )
    file_mime_type                                  = models.CharField( max_length = 255 )
    file_format                                     = models.CharField( max_length = 255 )
    file_size                                       = models.CharField( max_length = 255 )
    file_type                                       = models.CharField( max_length = 255 )
    file_function                                   = models.CharField( max_length = 255 )
    file_checksum                                   = models.CharField( max_length = 255 )
    file_checksum_type                              = models.CharField( max_length = 255 )
    file_transform_type                             = models.CharField( max_length = 255 )
    file_transform_key                              = models.CharField( max_length = 255 )
    comments                                        = models.CharField( max_length = 255 )
    aic_id                                          = models.CharField( max_length = 255 ) # Additional metadata for information package
    projectname                                     = models.CharField( max_length = 255 )
    policyid                                        = models.IntegerField( default=0 )
    receipt_email                                   = models.CharField( max_length = 255 )


    class Meta:
        ordering = ['type']
    verbose_name = 'IP Parameter'
        
    def __unicode__(self):
        # create a unicode representation of this object
        return self.type

    def populate_from_form(self, form):
        # pull out all fields from a form and use them to set
        # the values of this object.
        for field in IPParameter._meta.fields:
            if field.name in form.cleaned_data:
                setattr( self, field.name, form.cleaned_data[field.name] )

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self) 
                 for field in IPParameter._meta.fields }



