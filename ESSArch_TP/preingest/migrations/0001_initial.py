# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveObject',
            fields=[
                ('ObjectUUID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256)),
                ('progress', models.IntegerField(blank=True, default=0)),
                ('type', models.IntegerField(choices=[(-1, 'Undefined'), (0, 'Success'), (1, 'Error'), (2, 'Warning')], null=True)),
                ('user', models.CharField(max_length=45)),
                ('result', picklefield.fields.PickledObjectField(blank=True, editable=False)),
                ('status', models.IntegerField(blank=True, choices=[(-1, 'Undefined'), (0, 'Success'), (1, 'Error'), (2, 'Warning')], default=0)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('hidden', models.BooleanField(default=False)),
                ('archiveobject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preingest.ArchiveObject')),
            ],
            options={
                'db_table': 'ProcessStep',
            },
        ),
        migrations.CreateModel(
            name='ProcessTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256)),
                ('progress', models.IntegerField(blank=True, default=0)),
                ('task_id', models.CharField(max_length=255, unique=True, verbose_name='task id')),
                ('status', models.CharField(choices=[(b'RECEIVED', b'RECEIVED'), (b'RETRY', b'RETRY'), (b'REVOKED', b'REVOKED'), (b'SUCCESS', b'SUCCESS'), (b'STARTED', b'STARTED'), (b'FAILURE', b'FAILURE'), (b'PENDING', b'PENDING')], default=b'PENDING', max_length=50, verbose_name='state')),
                ('result', picklefield.fields.PickledObjectField(default=None, editable=False, null=True)),
                ('date_done', models.DateTimeField(auto_now=True, verbose_name='done at')),
                ('traceback', models.TextField(blank=True, null=True, verbose_name='traceback')),
                ('hidden', models.BooleanField(db_index=True, default=False, editable=False)),
                ('meta', picklefield.fields.PickledObjectField(default=None, editable=False, null=True)),
                ('processstep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preingest.ProcessStep')),
            ],
            options={
                'db_table': 'ProcessTask',
            },
        ),
    ]