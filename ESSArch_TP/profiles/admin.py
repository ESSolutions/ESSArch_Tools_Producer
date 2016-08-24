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
                             ProfileTransferProject, ProfileTransferProjectRel, 
                             ProfileContentType, ProfileContentTypeRel,  
                             ProfileDataSelection, ProfileDataSelectionRel,
                             ProfileClassification, ProfileClassificationRel, 
                             ProfileImport, ProfileImportRel, 
                             ProfileSubmitDescription, ProfileSubmitDescriptionRel,
                             ProfileSIP, ProfileSIPRel,
                             ProfileAIP, ProfileAIPRel,
                             ProfileDIP, ProfileDIPRel, 
                             ProfileWorkflow, ProfileWorkflowRel,
                             ProfilePreservationMetadata, ProfilePreservationMetadataRel,
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
Profile Transfer Project
"""
class ProfileTransferProjectAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_transfer_project_name', 'profile_transfer_project_type', 'profile_transfer_project_status', 'profile_transfer_project_label' )
    search_fields = ( 'profile_transfer_project_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_transfer_project_name', 'profile_transfer_project_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
			      'id', #'profile_transfer_project',
			      'profile_transfer_project_name',
			      'profile_transfer_project_type',
			      'profile_transfer_project_status',
			      'profile_transfer_project_label',
                              )}),
                ('Transfer project specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_transfer_project_specification',
                              'profile_transfer_project_data',
                              )}),
                )

admin.site.register(ProfileTransferProject, ProfileTransferProjectAdmin)


"""
Profile Content Type
"""
class ProfileContentTypeAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_content_type_name', 'profile_content_type_type', 'profile_content_type_status', 'profile_content_type_label' )
    search_fields = ( 'profile_content_type_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_content_type_name', 'profile_content_type_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
			      'id', #'profile_content_type',
			      'profile_content_type_name',
			      'profile_content_type_type',
			      'profile_content_type_status',
			      'profile_content_type_label',
                              )}),
                ('Content type specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
			      'profile_content_type_specification',
			      'profile_content_type_data',
                              )}),
                )

admin.site.register(ProfileContentType, ProfileContentTypeAdmin)


"""
Profile Data Selection
"""
class ProfileDataSelectionAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_data_selection_name', 'profile_data_selection_type', 'profile_data_selection_status', 'profile_data_selection_label' )
    search_fields = ( 'profile_data_selection_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_data_selection_name', 'profile_data_selection_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_data_selection',
                              'profile_data_selection_name',
                              'profile_data_selection_type',
                              'profile_data_selection_status',
                              'profile_data_selection_label',
                              )}),
                ('Data selection specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_data_selection_specification',
                              'profile_data_selection_data',
                              )}),
                )

admin.site.register(ProfileDataSelection, ProfileDataSelectionAdmin)


"""
Profile Classification
"""
class ProfileClassificationAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_classification_name', 'profile_classification_type', 'profile_classification_status', 'profile_classification_label' )
    search_fields = ( 'profile_classification_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_classification_name', 'profile_classification_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_classification',
                              'profile_classification_name',
                              'profile_classification_type',
                              'profile_classification_status',
                              'profile_classification_label',
                              )}),
                ('Classification specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_classification_specification',
                              'profile_classification_data',
                              )}),
                )

admin.site.register(ProfileClassification, ProfileClassificationAdmin)


"""
Profile Import
"""
class ProfileImportAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_import_name', 'profile_import_type', 'profile_import_status', 'profile_import_label' )
    search_fields = ( 'profile_import_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_import_name', 'profile_import_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_import',
                              'profile_import_name',
                              'profile_import_type',
                              'profile_import_status',
                              'profile_import_label',
                              )}),
                ('Import specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_import_specification',
                              'profile_import_data',
                              )}),
                )

admin.site.register(ProfileImport, ProfileImportAdmin)


"""
Profile Submit Description
"""
class ProfileSubmitDescriptionAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_sd_name', 'profile_sd_type', 'profile_sd_status', 'profile_sd_label' )
    search_fields = ( 'profile_sd_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_sd_name', 'profile_sd_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_submit_description',
                              'profile_sd_name',
                              'profile_sd_type',
                              'profile_sd_status',
                              'profile_sd_label',
                              )}),
                ('Submit description specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_sd_specification',
                              'profile_sd_data',
                              )}),
                )

admin.site.register(ProfileSubmitDescription, ProfileSubmitDescriptionAdmin)


"""
Profile SIP (Submission Information Package)
"""
class ProfileSIPAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_sip_name', 'profile_sip_type', 'profile_sip_status', 'profile_sip_label' )
    search_fields = ( 'profile_sip_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_sip_name', 'profile_sip_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_sip',
                              'profile_sip_name',
                              'profile_sip_type',
                              'profile_sip_status',
                              'profile_sip_label',
                              'sip_representation_info',
                              'sip_preservation_descriptive_info',
                              'sip_supplemental',
                              'sip_access_constraints',
                              'sip_datamodel_reference',
                              'sip_additional',
                              'sip_submission_method',
                              'sip_submission_schedule',
                              'sip_submission_data_inventory',
                              )}),
                ('SIP physcial and logical structure',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'sip_structure',
                              )}),
                ('SIP specification structure and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'sip_specification',
                              'sip_specification_data',
                              )}),
                )

admin.site.register(ProfileSIP, ProfileSIPAdmin)


"""
Profile AIP (Archival Information Package)
"""
class ProfileAIPAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_aip_name', 'profile_aip_type', 'profile_aip_status', 'profile_aip_label' )
    search_fields = ( 'profile_aip_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_aip_name', 'profile_aip_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_aip',
                              'profile_aip_name',
                              'profile_aip_type',
                              'profile_aip_status',
                              'profile_aip_label',
                              'aip_representation_info',
                              'aip_preservation_descriptive_info',
                              'aip_supplemental',
                              'aip_access_constraints',
                              'aip_datamodel_reference',
                              'aip_additional',
                              'aip_submission_method',
                              'aip_submission_schedule',
                              'aip_submission_data_inventory',
                              )}),
                ('AIP physcial and logical structure',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'aip_structure',
                              )}),
                ('AIP specification structure and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'aip_specification',
                              'aip_specification_data',
                              )}),
                )

admin.site.register(ProfileAIP, ProfileAIPAdmin)


"""
Profile DIP (Dissemination Information Package)
"""
class ProfileDIPAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_dip_name', 'profile_dip_type', 'profile_dip_status', 'profile_dip_label' )
    search_fields = ( 'profile_dip_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_dip_name', 'profile_dip_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_dip',
                              'profile_dip_name',
                              'profile_dip_type',
                              'profile_dip_status',
                              'profile_dip_label',
                              'dip_representation_info',
                              'dip_preservation_descriptive_info',
                              'dip_supplemental',
                              'dip_access_constraints',
                              'dip_datamodel_reference',
                              'dip_additional',
                              'dip_submission_method',
                              'dip_submission_schedule',
                              'dip_submission_data_inventory',
                              )}),
                ('DIP physcial and logical structure',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'dip_structure',
                              )}),
                ('DIP specification structure and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'dip_specification',
                              'dip_specification_data',
                              )}),
                )

admin.site.register(ProfileDIP, ProfileDIPAdmin)


"""
Profile Workflow
"""
class ProfileWorkflowAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_workflow_name', 'profile_workflow_type', 'profile_workflow_status', 'profile_workflow_label' )
    search_fields = ( 'profile_workflow_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_workflow_name', 'profile_workflow_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', #'profile_workflow',
                              'profile_workflow_name',
                              'profile_workflow_type',
                              'profile_workflow_status',
                              'profile_workflow_label',
                              )}),
                ('Workflow specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_workflow_specification',
                              'profile_workflow_data',
                              )}),
                )

admin.site.register(ProfileWorkflow, ProfileWorkflowAdmin)


"""
Profile Preservation Metadata
"""
class ProfilePreservationMetadataAdmin( admin.ModelAdmin ):
    list_display = ( 'profile_preservation_metadata_name', 'profile_preservation_metadata_type', 'profile_preservation_metadata_status', 'profile_preservation_metadata_label' )
    search_fields = ( 'profile_preservation_metadata_name', )
    readonly_fields = ('id',)
    list_filter = ('profile_preservation_metadata_name', 'profile_preservation_metadata_label')
    #fields = ('entity', 'value')
    fieldsets = (
                (None,{
                   'classes': ('wide'),
                   'fields': (
                              'id', 
                              'profile_preservation_metadata_name',
                              'profile_preservation_metadata_type',
                              'profile_preservation_metadata_status',
                              'profile_preservation_metadata_label',
                              )}),
                ('Preservation Metadata specification and data',{
                   'classes': ('collapse','wide'),
                   'fields': (
                              'profile_preservation_metadata_specification',
                              'profile_preservation_metadata_data',
                              )}),
                )

admin.site.register(ProfilePreservationMetadata, ProfilePreservationMetadataAdmin)

