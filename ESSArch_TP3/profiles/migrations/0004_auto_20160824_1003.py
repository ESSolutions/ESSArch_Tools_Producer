# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20160823_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileAIPRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profileaip', models.ForeignKey(to='profiles.ProfileAIP')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileAIP',
            },
        ),
        migrations.CreateModel(
            name='ProfileClassificationRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profileclassification', models.ForeignKey(to='profiles.ProfileClassification')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileClassification',
            },
        ),
        migrations.CreateModel(
            name='ProfileContentTypeRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profilecontenttype', models.ForeignKey(to='profiles.ProfileContentType')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileContentType',
            },
        ),
        migrations.CreateModel(
            name='ProfileDataSelectionRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profiledataselection', models.ForeignKey(to='profiles.ProfileDataSelection')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileDataSelection',
            },
        ),
        migrations.CreateModel(
            name='ProfileDIPRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profiledip', models.ForeignKey(to='profiles.ProfileDIP')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileDIP',
            },
        ),
        migrations.CreateModel(
            name='ProfileImportRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profileimport', models.ForeignKey(to='profiles.ProfileImport')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileImport',
            },
        ),
        migrations.CreateModel(
            name='ProfilePreservationMetadataRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profilepreservationmetadata', models.ForeignKey(to='profiles.ProfilePreservationMetadata')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfilePreservationMetadata',
            },
        ),
        migrations.CreateModel(
            name='ProfileSIPRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profilesip', models.ForeignKey(to='profiles.ProfileSIP')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileSIP',
            },
        ),
        migrations.CreateModel(
            name='ProfileSubmitDescriptionRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profilesubmitdescription', models.ForeignKey(to='profiles.ProfileSubmitDescription')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileSubmitDescription',
            },
        ),
        migrations.CreateModel(
            name='ProfileTransferProjectRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profiletransferproject', models.ForeignKey(to='profiles.ProfileTransferProject')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileTransferProject',
            },
        ),
        migrations.CreateModel(
            name='ProfileWorkflowRel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'Profile status', choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Default')])),
                ('profileworkflow', models.ForeignKey(to='profiles.ProfileWorkflow')),
            ],
            options={
                'ordering': ['status'],
                'verbose_name': 'ProfileWorkflow',
            },
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_aip',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_classification',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_content_type',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_data_selection',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_dip',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_import',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_preservation_metadata',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_sip',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_submit_description',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_transfer_project',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='default_profile_workflow',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_aip',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_classification',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_content_type',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_data_selection',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_dip',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_import',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_preservation_metadata',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_sip',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_submit_description',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_transfer_project',
        ),
        migrations.RemoveField(
            model_name='submissionagreement',
            name='profile_workflow',
        ),
        migrations.AddField(
            model_name='profileworkflowrel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profiletransferprojectrel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profilesubmitdescriptionrel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profilesiprel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profilepreservationmetadatarel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profileimportrel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profilediprel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profiledataselectionrel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profilecontenttyperel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profileclassificationrel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
        migrations.AddField(
            model_name='profileaiprel',
            name='submissionagreement',
            field=models.ForeignKey(to='profiles.SubmissionAgreement'),
        ),
    ]
