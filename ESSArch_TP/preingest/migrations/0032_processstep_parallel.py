# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-17 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preingest', '0031_auto_20160817_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='processstep',
            name='parallel',
            field=models.BooleanField(default=False),
        ),
    ]
