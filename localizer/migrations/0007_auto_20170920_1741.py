# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import localizer.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('localizer', '0006_auto_20170919_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='probe_control_conditions',
            field=models.CharField(default=localizer.models.create_control_condition_sequence, max_length=200),
        ),
    ]
