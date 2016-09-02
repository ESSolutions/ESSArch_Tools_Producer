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

import jsonfield

import uuid

Profile_Status_CHOICES = (
    (0, 'Disabled'),
    (1, 'Enabled'),
    (2, 'Default'),
)


class ProfileTransferProjectRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profiletransferproject = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileContentTypeRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profilecontenttype = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileDataSelectionRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profiledataselection = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileClassificationRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profileclassification = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileImportRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profileimport = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileSubmitDescriptionRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profilesubmitdescription = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileSIPRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profilesip = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileAIPRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profileaip = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileDIPRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profiledip = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfileWorkflowRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profileworkflow = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class ProfilePreservationMetadataRel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        'Profile status',
        choices=Profile_Status_CHOICES,
        default=0
    )
    profilepreservationmetadata = models.ForeignKey('Profile')
    submissionagreement = models.ForeignKey('SubmissionAgreement')

    class Meta:
        verbose_name = 'ProfileRel'
        ordering = ['status']

    def __unicode__(self):
        return unicode(self.id)


class SubmissionAgreement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    sa_name = models.CharField(max_length=255)
    sa_type = models.CharField(max_length=255)
    sa_status = models.CharField(max_length=255)
    sa_label = models.CharField(max_length=255)
    sa_cm_version = models.CharField(max_length=255)
    sa_cm_release_date = models.CharField(max_length=255)
    sa_cm_change_authority = models.CharField(max_length=255)
    sa_cm_change_description = models.CharField(max_length=255)
    sa_cm_sections_affected = models.CharField(max_length=255)
    sa_producer_organization = models.CharField(max_length=255)
    sa_producer_main_name = models.CharField(max_length=255)
    sa_producer_main_address = models.CharField(max_length=255)
    sa_producer_main_phone = models.CharField(max_length=255)
    sa_producer_main_email = models.CharField(max_length=255)
    sa_producer_main_additional = models.CharField(max_length=255)
    sa_producer_individual_name = models.CharField(max_length=255)
    sa_producer_individual_role = models.CharField(max_length=255)
    sa_producer_individual_phone = models.CharField(max_length=255)
    sa_producer_individual_email = models.CharField(max_length=255)
    sa_producer_individual_additional = models.CharField(max_length=255)
    sa_archivist_organization = models.CharField(max_length=255)
    sa_archivist_main_name = models.CharField(max_length=255)
    sa_archivist_main_address = models.CharField(max_length=255)
    sa_archivist_main_phone = models.CharField(max_length=255)
    sa_archivist_main_email = models.CharField(max_length=255)
    sa_archivist_main_additional = models.CharField(max_length=255)
    sa_archivist_individual_name = models.CharField(max_length=255)
    sa_archivist_individual_role = models.CharField(max_length=255)
    sa_archivist_individual_phone = models.CharField(max_length=255)
    sa_archivist_individual_email = models.CharField(max_length=255)
    sa_archivist_individual_additional = models.CharField(max_length=255)
    sa_designated_community_description = models.CharField(max_length=255)
    sa_designated_community_individual_name = models.CharField(max_length=255)
    sa_designated_community_individual_role = models.CharField(max_length=255)
    sa_designated_community_individual_phone = models.CharField(max_length=255)
    sa_designated_community_individual_email = models.CharField(max_length=255)
    sa_designated_community_individual_additional = models.CharField(
        max_length=255
    )

    profile_transfer_project = models.ManyToManyField(
        'Profile',
        related_name='profile_transfer_project',
        through='ProfileTransferProjectRel',
        through_fields=('submissionagreement', 'profiletransferproject')
    )
    profile_content_type = models.ManyToManyField(
        'Profile',
        related_name='profile_content_type',
        through='ProfileContentTypeRel',
        through_fields=('submissionagreement', 'profilecontenttype')
    )

    profile_data_selection = models.ManyToManyField(
        'Profile',
        related_name='profile_data_selection',
        through='ProfileDataSelectionRel',
        through_fields=('submissionagreement', 'profiledataselection')
    )
    profile_classification = models.ManyToManyField(
        'Profile',
        related_name='profile_classification',
        through='ProfileClassificationRel',
        through_fields=('submissionagreement', 'profileclassification')
    )
    profile_import = models.ManyToManyField(
        'Profile',
        related_name='profile_import',
        through='ProfileImportRel',
        through_fields=('submissionagreement', 'profileimport')
    )
    profile_submit_description = models.ManyToManyField(
        'Profile',
        related_name='profile_submit_description',
        through='ProfileSubmitDescriptionRel',
        through_fields=('submissionagreement', 'profilesubmitdescription')
    )
    profile_sip = models.ManyToManyField(
        'Profile',
        related_name='profile_sip',
        through='ProfileSIPRel',
        through_fields=('submissionagreement', 'profilesip')
    )
    profile_aip = models.ManyToManyField(
        'Profile',
        related_name='profile_aip',
        through='ProfileAIPRel',
        through_fields=('submissionagreement', 'profileaip')
    )
    profile_dip = models.ManyToManyField(
        'Profile',
        related_name='profile_dip',
        through='ProfileDIPRel',
        through_fields=('submissionagreement', 'profiledip')
    )
    profile_workflow = models.ManyToManyField(
        'Profile',
        related_name='profile_workflow',
        through='ProfileWorkflowRel',
        through_fields=('submissionagreement', 'profileworkflow')
    )
    profile_preservation_metadata = models.ManyToManyField(
        'Profile',
        related_name='profile_preservation_metadata',
        through='ProfilePreservationMetadataRel',
        through_fields=('submissionagreement', 'profilepreservationmetadata')
    )

    class Meta:
        ordering = ["sa_name"]
        verbose_name = 'Submission Agreement'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.sa_name, self.id)

    """
    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return {field.name: field.value_to_string(self)
                for field in SubmissionAgreement._meta.fields}
    """

profile_types = [
    "Transfer Project",
    "Content Type",
    "Data Selection",
    "Classification",
    "Import",
    "Submit Description",
    "SIP",
    "AIP",
    "DIP",
    "Workflow",
    "Preservation Description",
]

PROFILE_TYPE_CHOICES = zip(
    [p.replace(' ', '_').lower() for p in profile_types],
    profile_types
)


class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    profile_type = models.CharField(
        max_length=255,
        choices=PROFILE_TYPE_CHOICES
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    representation_info = models.CharField(max_length=255)
    preservation_descriptive_info = models.CharField(max_length=255)
    supplemental = models.CharField(max_length=255)
    access_constraints = models.CharField(max_length=255)
    datamodel_reference = models.CharField(max_length=255)
    additional = models.CharField(max_length=255)
    submission_method = models.CharField(max_length=255)
    submission_schedule = models.CharField(max_length=255)
    submission_data_inventory = models.CharField(max_length=255)
    structure = models.TextField()
    template = jsonfield.JSONField(null=True)
    specification = jsonfield.JSONField(null=True)
    specification_data = jsonfield.JSONField(null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = 'Profile'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s (%s) - %s' % (self.name, self.profile_type, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return {field.name: field.value_to_string(self)
                for field in Profile._meta.fields}
