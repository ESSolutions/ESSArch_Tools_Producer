#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
"""
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
"""

from django.contrib import admin

from profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileTransferProjectRel,
    ProfileContentTypeRel,
    ProfileDataSelectionRel,
    ProfileClassificationRel,
    ProfileImportRel,
    ProfileSubmitDescriptionRel,
    ProfileSIPRel,
    ProfileAIPRel,
    ProfileDIPRel,
    ProfileWorkflowRel,
    ProfilePreservationMetadataRel,
)

class profile_transfer_project_Inline(admin.TabularInline):
    model = ProfileTransferProjectRel
    extra = 0

class  profile_content_type_Inline(admin.TabularInline):
    model = ProfileContentTypeRel
    extra = 0
    
class profile_data_selection_Inline(admin.TabularInline):
    model = ProfileDataSelectionRel
    extra = 0

class profile_classification_Inline(admin.TabularInline):
    model = ProfileClassificationRel
    extra = 0

class profile_import_Inline(admin.TabularInline):
    model = ProfileImportRel
    extra = 0

class profile_submit_description_Inline(admin.TabularInline):
    model = ProfileSubmitDescriptionRel
    extra = 0
    
class profile_sip_Inline(admin.TabularInline):
    model = ProfileSIPRel
    extra = 0
    
class profile_aip_Inline(admin.TabularInline):
    model = ProfileAIPRel
    extra = 0

class profile_dip_Inline(admin.TabularInline):
    model = ProfileDIPRel
    extra = 0

class profile_workflow_Inline(admin.TabularInline):
    model = ProfileWorkflowRel
    extra = 0

class profile_preservation_metadata_Inline(admin.TabularInline):
    model = ProfilePreservationMetadataRel
    extra = 0

"""
Submission Agreement
"""
class SubmissionAgreementAdmin( admin.ModelAdmin ):
    list_display = ( 'sa_name', 'sa_type', 'sa_status', 'sa_label' )
    search_fields = ( 'sa_name', )
    readonly_fields = ('id',)
    list_filter = ('sa_name', 'sa_type')
    #fields = ('entity', 'value')
    inlines = (
               profile_transfer_project_Inline,
               profile_content_type_Inline,
               profile_data_selection_Inline,
               profile_classification_Inline,
               profile_import_Inline,
               profile_submit_description_Inline,
               profile_sip_Inline,
               profile_aip_Inline,
               profile_dip_Inline,
               profile_workflow_Inline,
               profile_preservation_metadata_Inline,
               )
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'submission_agreement',
            			      'sa_name',
            			      'sa_type',
            			      'sa_status',
            			      'sa_label',
                              )}),
                ('Change management',{
                   'classes': ('collapse','wide'),
                   'fields': (
			      'sa_cm_version',
			      'sa_cm_release_date',
			      'sa_cm_change_authority',
			      'sa_cm_change_description',
			      'sa_cm_sections_affected'
                              )}),
                ('Informaton about Producer organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
			      'sa_producer_organization',
			      'sa_producer_main_name',
	 		      'sa_producer_main_address',
			      'sa_producer_main_phone',
		   	      'sa_producer_main_email',
			      'sa_producer_main_additional',
			      'sa_producer_individual_name',
			      'sa_producer_individual_role',
			      'sa_producer_individual_phone',
			      'sa_producer_individual_email',
			      'sa_producer_individual_additional',
			      )}),
                ('Information about Archival organization',{
                   'classes': ('collapse','wide'),
                   'fields': (
			      'sa_archivist_organization',
			      'sa_archivist_main_name',
			      'sa_archivist_main_address',
			      'sa_archivist_main_phone',
			      'sa_archivist_main_email',
			      'sa_archivist_main_additional',
			      'sa_archivist_individual_name',
			      'sa_archivist_individual_role',
			      'sa_archivist_individual_phone',
			      'sa_archivist_individual_email',
			      'sa_archivist_individual_additional',
			      )}),
                ('Information about designated community',{
                   'classes': ('collapse','wide'),
                   'fields': (
			      'sa_designated_community_description',
			      'sa_designated_community_individual_name',
			      'sa_designated_community_individual_role',
			      'sa_designated_community_individual_phone',
			      'sa_designated_community_individual_email',
			      'sa_designated_community_individual_additional',
                              )}),
                 
#                ('Profiles',{
#                  'classes': ('collapse','wide'),
#                   'fields': (
#                              inlines = (profile_transfer_project_Inline,)
#			      'profile_transfer_project',
#			      'profile_content_type',
#			      'profile_data_selection',
#			      'profile_classification',
#			      'profile_import',
#			      'profile_submit_description',
#                              )}),
#                ('Information Packages Characteristics',{
#                   'classes': ('collapse','wide'),
#                   'fields': (
#			      'profile_sip',
#			      'profile_aip',
#			      'profile_dip',
#                              )}),
#                ('Workflows',{
#                   'classes': ('collapse','wide'),
#                   'fields': (
#			      'profile_workflow',
#                              )}),
#                ('Preservation metadata',{
#                   'classes': ('collapse','wide'),
#                   'fields': (
#                              'profile_preservation_metadata',
#                              )}),
                )

admin.site.register(SubmissionAgreement, SubmissionAgreementAdmin)

"""
Profile
"""
class ProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'type', 'status', 'label' )
    search_fields = ( 'name', )
    readonly_fields = ('id',)
    list_filter = ('name', 'label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id',
                              'profile_type',
                              'name',
                              'type',
                              'status',
                              'label',
                              'representation_info',
                              'preservation_descriptive_info',
                              'supplemental',
                              'access_constraints',
                              'datamodel_reference',
                              'additional',
                              'submission_method',
                              'submission_schedule',
                              'submission_data_inventory',
                              )}),
                ('physcial and logical structure',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'structure',
                              )}),
                ('specification structure and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'specification',
                              'specification_data',
                              )}),
                )

admin.site.register(Profile, ProfileAdmin)
