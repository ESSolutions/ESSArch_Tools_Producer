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

from profiles.models import AgentProfile, TransferProjectProfile, ImportProfile, DataSelectionProfile, ClassificationProfile
from django.contrib import admin

# Agent Profiles
class AgentProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'agent_profile', 'agent_profile_id', 'label', 'submission_agreement' )
    search_fields = ( 'agent_profile', )
    #readonly_fields = ('entity',)
    list_filter = ('agent_profile', 'label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'agent_profile',
			      'agent_profile_id',
			      'agent_profile_type',
			      'agent_profile_status',
			      'label',
			      'submission_agreement'
                              )}),
                ('Metadata for Archivist organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'archivist_organization',
                              'archivist_organization_id',
                              'archivist_organization_software',
                              'archivist_organization_software_id',
                              'archivist_organization_software_type',
                              'archivist_organization_software_type_version',
                              'archivist_individual',
                              'archivist_individual_telephone',
                              'archivist_individual_email',
                              )}),
                ('Metadata for Creator organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'creator_organization',
                              'creator_organization_id',
                              'creator_individual',
                              'creator_individual_details',
                              'creator_individual_telephone',
                              'creator_individual_email',
                              'creator_software',
                              'creator_software_id',
                              )}),
                ('Metadata for Producer organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'producer_organization',
                              'producer_organization_id',
                              'producer_individual',
                              'producer_individual_telephone',
                              'producer_individual_email',
                              'producer_organization_software',
                              'producer_organization_software_identity',
                              'producer_organization_software_type',
                              'producer_organization_software_type_version',
                              )}),
                ('Metadata for Submitter organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'submitter_organization',
                              'submitter_organization_id',
                              'submitter_individual',
                              'submitter_individual_telephone',
                              'submitter_individual_email',
                              )}),
                ('Metadata for IPowner organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'ipowner_organization',
                              'ipowner_organization_id',
                              'ipowner_individual',
                              'ipowner_individual_telephone',
                              'ipowner_individual_email',
                              )}),
                ('Metadata for Editor organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'editor_organization',
                              'editor_organization_id',
                              )}),
                ('Metadata for Preservation organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'preservation_organization',
                              'preservation_organization_id',
                              'preservation_organization_software',
                              'preservation_organization_software_id',
                              )}),
		) 

admin.site.register(AgentProfile, AgentProfileAdmin)

# Transfer Project Profiles
class TransferProjectProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'transfer_project_profile', 'transfer_project_profile_id', 'label', 'submission_agreement' )
    search_fields = ( 'transfer_project_profile', )
    #readonly_fields = ('entity',)
    list_filter = ('transfer_project_profile', 'label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'transfer_project_profile',
                              'transfer_project_profile_id',
                              'transfer_project_profile_type',
                              'transfer_project_profile_status',
                              'label',
                              'submission_agreement'
                              )}),
                ('Metadata for transer project',{
                   'classes': ('collapse','wide'),
                   'fields': (
          		      'system_type',
          		      'previous_submission_agreement',
          		      'data_submission_session',
          		      'package_number',
          		      'referencecode',
          		      'previous_referencecode',
          		      'appraisal',
          		      'accessrestrict',
          		      'archive_policy',
          		      'container_format',
          		      'container_format_compression',
          		      'informationclass',
                              )}),
                )

admin.site.register(TransferProjectProfile, TransferProjectProfileAdmin)

# Import Profiles
class ImportProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'import_profile', 'import_profile_id', 'label', 'submission_agreement' )
    search_fields = ( 'import_profile', )
    #readonly_fields = ('entity',)
    list_filter = ('import_profile', 'label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'import_profile',
                              'import_profile_id',
                              'import_profile_type',
                              'import_profile_status',
                              'label',
                              'submission_agreement'
                              )}),
                )

admin.site.register(ImportProfile, ImportProfileAdmin)

# Data Selection Profiles
class DataSelectionProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'data_selection_profile', 'data_selection_profile_id', 'label', 'submission_agreement' )
    search_fields = ( 'data_selection_profile', )
    #readonly_fields = ('entity',)
    list_filter = ('data_selection_profile', 'label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'data_selection_profile',
                              'data_selection_profile_id',
                              'data_selection_profile_type',
                              'data_selection_profile_status',
                              'label',
                              'submission_agreement'
                              )}),
                )

admin.site.register(DataSelectionProfile, DataSelectionProfileAdmin)

# Classification Profiles
class ClassificationProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'classification_profile', 'classification_profile_id', 'label', 'submission_agreement' )
    search_fields = ( 'classification_profile', )
    #readonly_fields = ('entity',)
    list_filter = ('classification_profile', 'label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'classification_profile',
                              'classification_profile_id',
                              'classification_profile_type',
                              'classification_profile_status',
                              'label',
                              'submission_agreement'
                              )}),
                )

admin.site.register(ClassificationProfile, ClassificationProfileAdmin)

