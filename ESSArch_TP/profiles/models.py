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
from django.forms.utils import flatatt
from django import forms

import sys, datetime


# Agent Profiles
class AgentProfile(models.Model):
    agent_profile	                            = models.CharField( max_length = 255 )
    agent_profile_id	                            = models.CharField( max_length = 255 )
    agent_profile_type   	                    = models.CharField( max_length = 255 )
    agent_profile_status    		            = models.CharField( max_length = 255 )
    label		                            = models.CharField( max_length = 255 )
    submission_agreement                            = models.CharField( max_length = 255 )
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

    class Meta:
        ordering = ["archivist_organization"]

    def __unicode__(self):
        # create a unicode representation of this object
        return self.agent_profile

    def populate_from_form(self, form):
        # pull out all fields from a form and use them to set
        # the values of this object.
        for field in AgentProfile._meta.fields:
            if field.name in form.cleaned_data:
                setattr( self, field.name, form.cleaned_data[field.name] )

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in AgentProfile._meta.fields }


# Transfer Project Profiles
class TransferProjectProfile(models.Model):
    transfer_project_profile                        = models.CharField( max_length = 255 )
    transfer_project_profile_id                     = models.CharField( max_length = 255 )
    transfer_project_profile_type	            = models.CharField( max_length = 255 )
    transfer_project_profile_status	            = models.CharField( max_length = 255 )
    label                                           = models.CharField( max_length = 255 )
    system_type                                     = models.CharField( max_length = 255 )
    submission_agreement                            = models.CharField( max_length = 255 )
    previous_submission_agreement                   = models.CharField( max_length = 255 )
    data_submission_session                         = models.CharField( max_length = 255 )
    package_number                                  = models.CharField( max_length = 255 )
    referencecode                                   = models.CharField( max_length = 255 )
    previous_referencecode                          = models.CharField( max_length = 255 )
    appraisal                                       = models.CharField( max_length = 255 )
    accessrestrict                                  = models.CharField( max_length = 255 )
    archive_policy                                  = models.CharField( max_length = 255 )
    container_format                                = models.CharField( max_length = 255 )
    container_format_compression                    = models.CharField( max_length = 255 )
    informationclass                                = models.CharField( max_length = 255 )

    class Meta:
        ordering = ["transfer_project_profile"]

    def __unicode__(self):
        # create a unicode representation of this object
        return self.transfer_project_profile

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in TransferProjectProfile._meta.fields }


# Import Profiles
class ImportProfile(models.Model):
    import_profile                        	    = models.CharField( max_length = 255 )
    import_profile_id  		                    = models.CharField( max_length = 255 )
    import_profile_type                             = models.CharField( max_length = 255 )
    import_profile_status                           = models.CharField( max_length = 255 )
    label                                           = models.CharField( max_length = 255 )
    submission_agreement                            = models.CharField( max_length = 255 )

    class Meta:
        ordering = ["import_profile"]

    def __unicode__(self):
        # create a unicode representation of this object
        return self.import_profile

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ImportProfile._meta.fields }


# Data Selection Profiles
class DataSelectionProfile(models.Model):
    data_selection_profile      	            = models.CharField( max_length = 255 )
    data_selection_profile_id                       = models.CharField( max_length = 255 )
    data_selection_profile_type                     = models.CharField( max_length = 255 )
    data_selection_profile_status                   = models.CharField( max_length = 255 )
    label                                           = models.CharField( max_length = 255 )
    submission_agreement                            = models.CharField( max_length = 255 )

    class Meta:
        ordering = ["data_selection_profile"]

    def __unicode__(self):
        # create a unicode representation of this object
        return self.data_selection_profile

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in DataSelectionProfile._meta.fields }


# Classification Profiles
class ClassificationProfile(models.Model):
    classification_profile                          = models.CharField( max_length = 255 )
    classification_profile_id                       = models.CharField( max_length = 255 )
    classification_profile_type                     = models.CharField( max_length = 255 )
    classification_profile_status                   = models.CharField( max_length = 255 )
    label                                           = models.CharField( max_length = 255 )
    submission_agreement                            = models.CharField( max_length = 255 )

    class Meta:
        ordering = ["classification_profile"]

    def __unicode__(self):
        # create a unicode representation of this object
        return self.classification_profile

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ClassificationProfile._meta.fields }


