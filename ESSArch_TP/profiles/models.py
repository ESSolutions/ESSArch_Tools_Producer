"""
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2016  ES Solutions AB

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

from django.db import models

import uuid

"""
Submission Agreement
"""
class SubmissionAgreement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # submission_agreement
    sa_name					= models.CharField( max_length = 255 )
    sa_type					= models.CharField( max_length = 255 )
    sa_status					= models.CharField( max_length = 255 )
    sa_label					= models.CharField( max_length = 255 )
    sa_cm_version				= models.CharField( max_length = 255 )
    sa_cm_release_date				= models.CharField( max_length = 255 )
    sa_cm_change_authority			= models.CharField( max_length = 255 )
    sa_cm_change_description			= models.CharField( max_length = 255 )
    sa_cm_sections_affected			= models.CharField( max_length = 255 )
    sa_producer_organization			= models.CharField( max_length = 255 )
    sa_producer_main_name			= models.CharField( max_length = 255 )
    sa_producer_main_address			= models.CharField( max_length = 255 )
    sa_producer_main_phone			= models.CharField( max_length = 255 )
    sa_producer_main_email			= models.CharField( max_length = 255 )
    sa_producer_main_additional			= models.CharField( max_length = 255 )
    sa_producer_individual_name			= models.CharField( max_length = 255 )
    sa_producer_individual_role			= models.CharField( max_length = 255 )
    sa_producer_individual_phone		= models.CharField( max_length = 255 )
    sa_producer_individual_email		= models.CharField( max_length = 255 )
    sa_producer_individual_additional		= models.CharField( max_length = 255 )
    sa_archivist_organization			= models.CharField( max_length = 255 )
    sa_archivist_main_name			= models.CharField( max_length = 255 )
    sa_archivist_main_address			= models.CharField( max_length = 255 )
    sa_archivist_main_phone			= models.CharField( max_length = 255 )
    sa_archivist_main_email			= models.CharField( max_length = 255 )
    sa_archivist_main_additional		= models.CharField( max_length = 255 )
    sa_archivist_individual_name		= models.CharField( max_length = 255 )
    sa_archivist_individual_role		= models.CharField( max_length = 255 )
    sa_archivist_individual_phone		= models.CharField( max_length = 255 )
    sa_archivist_individual_email		= models.CharField( max_length = 255 )
    sa_archivist_individual_additional		= models.CharField( max_length = 255 )
    sa_designated_community_description		= models.CharField( max_length = 255 )
    sa_designated_community_individual_name	= models.CharField( max_length = 255 )
    sa_designated_community_individual_role	= models.CharField( max_length = 255 )
    sa_designated_community_individual_phone	= models.CharField( max_length = 255 )
    sa_designated_community_individual_email	= models.CharField( max_length = 255 )
    sa_designated_community_individual_additional	= models.CharField( max_length = 255 )
    profile_transfer_project			= models.ForeignKey('ProfileTransferProject', on_delete=models.CASCADE)
    profile_content_type			= models.ForeignKey('ProfileContentType', on_delete=models.CASCADE)
    profile_data_selection			= models.ForeignKey('ProfileDataSelection', on_delete=models.CASCADE)
    profile_classification			= models.ForeignKey('ProfileClassification', on_delete=models.CASCADE)
    profile_import				= models.ForeignKey('ProfileImport', on_delete=models.CASCADE)
    profile_submit_description			= models.ForeignKey('ProfileSubmitDescription', on_delete=models.CASCADE)
    profile_sip					= models.ForeignKey('ProfileSIP', on_delete=models.CASCADE)
    profile_aip					= models.ForeignKey('ProfileAIP', on_delete=models.CASCADE)
    profile_dip					= models.ForeignKey('ProfileDIP', on_delete=models.CASCADE)
    profile_workflow 				= models.ForeignKey('ProfileWorkflow', on_delete=models.CASCADE)
    profile_preservation_metadata		= models.CharField( max_length = 255, default='' )
    default_profile_transfer_project            = models.CharField( max_length = 255, default='')
    default_profile_content_type                = models.CharField( max_length = 255, default='' )
    default_profile_data_selection              = models.CharField( max_length = 255, default='' )
    default_profile_classification              = models.CharField( max_length = 255, default='' )
    default_profile_import                      = models.CharField( max_length = 255, default='' )
    default_profile_submit_description          = models.CharField( max_length = 255, default='' )
    default_profile_sip                         = models.CharField( max_length = 255, default='' )
    default_profile_aip                         = models.CharField( max_length = 255, default='' )
    default_profile_dip                         = models.CharField( max_length = 255, default='' )
    default_profile_workflow                    = models.CharField( max_length = 255, default='' )
    default_profile_preservation_metadata       = models.CharField( max_length = 255, default='' )

    class Meta:
        ordering = ["sa_name"]
        verbose_name = 'Submission Agreement'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.sa_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in SubmissionAgreement._meta.fields }


"""
Profile Transfer Project
"""
class ProfileTransferProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_transfer_project
    profile_transfer_project_name		= models.CharField( max_length = 255 )
    profile_transfer_project_type		= models.CharField( max_length = 255 )
    profile_transfer_project_status		= models.CharField( max_length = 255 )
    profile_transfer_project_label		= models.CharField( max_length = 255 )
    profile_transfer_project_specification	= models.TextField(default='')
    profile_transfer_project_data		= models.TextField(default='')

    class Meta:
        ordering = ["profile_transfer_project_name"]
        verbose_name = 'Profile Transfer Project'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_transfer_project_name, self.id) 

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileTransferProject._meta.fields }


"""
Profile Content Type
"""
class ProfileContentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_content_type
    profile_content_type_name		= models.CharField( max_length = 255 )
    profile_content_type_type		= models.CharField( max_length = 255 )
    profile_content_type_status		= models.CharField( max_length = 255 )
    profile_content_type_label		= models.CharField( max_length = 255 )
    profile_content_type_specification	= models.TextField()
    profile_content_type_data		= models.TextField(default='')

    class Meta:
        ordering = ["profile_content_type_name"]
        verbose_name = 'Profile Content Type'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_content_type_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileContentType._meta.fields }


"""
Profile Data Selection
"""
class ProfileDataSelection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_data_selection
    profile_data_selection_name		= models.CharField( max_length = 255 )
    profile_data_selection_type		= models.CharField( max_length = 255 )
    profile_data_selection_status	= models.CharField( max_length = 255 )
    profile_data_selection_label	= models.CharField( max_length = 255 )
    profile_data_selection_specification	= models.TextField()
    profile_data_selection_data		= models.TextField(default='')

    class Meta:
        ordering = ["profile_data_selection_name"]
        verbose_name = 'Profile Data Selection'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_data_selection_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileDataSelection._meta.fields }


"""
Profile Classification
"""
class ProfileClassification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_classification
    profile_classification_name		= models.CharField( max_length = 255 )
    profile_classification_type		= models.CharField( max_length = 255 )
    profile_classification_status	= models.CharField( max_length = 255 )
    profile_classification_label	= models.CharField( max_length = 255 )
    profile_classification_specification	= models.TextField()
    profile_classification_data		= models.TextField(default='')

    class Meta:
        ordering = ["profile_classification_name"]
        verbose_name = 'Profile Classification'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_classification_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileClassification._meta.fields }


"""
Profile Import
"""
class ProfileImport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_import
    profile_import_name         = models.CharField( max_length = 255 )
    profile_import_type         = models.CharField( max_length = 255 )
    profile_import_status       = models.CharField( max_length = 255 )
    profile_import_label	= models.CharField( max_length = 255 )
    profile_import_specification        = models.TextField()
    profile_import_data	        = models.TextField(default='')

    class Meta:
        ordering = ["profile_import_name"]
        verbose_name = 'Profile Import'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_import_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileImport._meta.fields }


"""
Profile Submit Description
"""
class ProfileSubmitDescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_submit_description
    profile_sd_name         	= models.CharField( max_length = 255 )
    profile_sd_type         	= models.CharField( max_length = 255 )
    profile_sd_status       	= models.CharField( max_length = 255 )
    profile_sd_label		= models.CharField( max_length = 255 )
    profile_sd_specification    = models.TextField()
    profile_sd_data		= models.TextField(default='')

    class Meta:
        ordering = ["profile_sd_name"]
        verbose_name = 'Profile Submit Description'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_sd_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileSubmitDescription._meta.fields }



"""
Profile SIP (Submission Information Package)
"""
class ProfileSIP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_sip
    profile_sip_name			= models.CharField( max_length = 255 )
    profile_sip_type			= models.CharField( max_length = 255 )
    profile_sip_status			= models.CharField( max_length = 255 )
    profile_sip_label			= models.CharField( max_length = 255 )
    sip_representation_info		= models.CharField( max_length = 255 )
    sip_preservation_descriptive_info	= models.CharField( max_length = 255 )
    sip_supplemental			= models.CharField( max_length = 255 )
    sip_access_constraints		= models.CharField( max_length = 255 )
    sip_datamodel_reference		= models.CharField( max_length = 255 )
    sip_additional			= models.CharField( max_length = 255 )
    sip_submission_method		= models.CharField( max_length = 255 )
    sip_submission_schedule		= models.CharField( max_length = 255 )
    sip_submission_data_inventory	= models.CharField( max_length = 255 )
    sip_structure                       = models.TextField()
    sip_specification			= models.TextField()
    sip_specification_data		= models.TextField()

    class Meta:
        ordering = ["profile_sip_name"]
        verbose_name = 'Profile SIP'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_sip_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileSIP._meta.fields }


"""
Profile AIP (Archival Information Package)
"""
class ProfileAIP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_aip
    profile_aip_name                    = models.CharField( max_length = 255 )
    profile_aip_type                    = models.CharField( max_length = 255 )
    profile_aip_status                  = models.CharField( max_length = 255 )
    profile_aip_label                   = models.CharField( max_length = 255 )
    aip_representation_info             = models.CharField( max_length = 255 )
    aip_preservation_descriptive_info   = models.CharField( max_length = 255 )
    aip_supplemental                    = models.CharField( max_length = 255 )
    aip_access_constraints              = models.CharField( max_length = 255 )
    aip_datamodel_reference             = models.CharField( max_length = 255 )
    aip_additional                      = models.CharField( max_length = 255 )
    aip_submission_method               = models.CharField( max_length = 255 )
    aip_submission_schedule             = models.CharField( max_length = 255 )
    aip_submission_data_inventory       = models.CharField( max_length = 255 )
    aip_structure                       = models.TextField()
    aip_specification                   = models.TextField()
    aip_specification_data              = models.TextField()

    class Meta:
        ordering = ["profile_aip_name"]
        verbose_name = 'Profile AIP'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_aip_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileAIP._meta.fields }


"""
Profile DIP (Dissemination Information Package)
"""
class ProfileDIP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_dip
    profile_dip_name                    = models.CharField( max_length = 255 )
    profile_dip_type                    = models.CharField( max_length = 255 )
    profile_dip_status                  = models.CharField( max_length = 255 )
    profile_dip_label                   = models.CharField( max_length = 255 )
    dip_representation_info             = models.CharField( max_length = 255 )
    dip_preservation_descriptive_info   = models.CharField( max_length = 255 )
    dip_supplemental                    = models.CharField( max_length = 255 )
    dip_access_constraints              = models.CharField( max_length = 255 )
    dip_datamodel_reference             = models.CharField( max_length = 255 )
    dip_additional                      = models.CharField( max_length = 255 )
    dip_submission_method               = models.CharField( max_length = 255 )
    dip_submission_schedule             = models.CharField( max_length = 255 )
    dip_submission_data_inventory       = models.CharField( max_length = 255 )
    dip_structure                       = models.TextField()
    dip_specification                   = models.TextField()
    dip_specification_data              = models.TextField()

    class Meta:
        ordering = ["profile_dip_name"]
        verbose_name = 'Profile DIP'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_dip_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileDIP._meta.fields }


"""
Profile Workflow
"""
class ProfileWorkflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_workflow
    profile_workflow_name		= models.CharField( max_length = 255 )
    profile_workflow_type		= models.CharField( max_length = 255 )
    profile_workflow_status		= models.CharField( max_length = 255 )
    profile_workflow_label		= models.CharField( max_length = 255 )
    profile_workflow_specification	= models.TextField()
    profile_workflow_data		= models.TextField(default='')

    class Meta:
        ordering = ["profile_workflow_name"]
        verbose_name = 'Profile Workflow'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_workflow_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfileWorkflow._meta.fields }

"""
Profile Preservation Metadata
"""
class ProfilePreservationMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # profile_workflow
    profile_preservation_metadata_name               = models.CharField( max_length = 255 )
    profile_preservation_metadata_type               = models.CharField( max_length = 255 )
    profile_preservation_metadata_status             = models.CharField( max_length = 255 )
    profile_preservation_metadata_label              = models.CharField( max_length = 255 )
    profile_preservation_metadata_specification      = models.TextField()
    profile_preservation_metadata_data               = models.TextField()

    class Meta:
        ordering = ["profile_preservation_metadata_name"]
        verbose_name = 'Profile Preservation Metadata'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.profile_preservation_metadata_name, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in ProfilePreservationMetadata._meta.fields }

