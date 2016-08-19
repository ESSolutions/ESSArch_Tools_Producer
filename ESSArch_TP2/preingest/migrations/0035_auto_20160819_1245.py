# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-19 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preingest', '0034_auto_20160818_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='eventApplication',
            new_name='application',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eventDateTime',
            new_name='dateTime',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eventDetail',
            new_name='detail',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eventOutcome',
            new_name='outcome',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eventOutcomeDetailNote',
            new_name='outcomeDetailNote',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eventType',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eventVersion',
            new_name='version',
        ),
    ]
