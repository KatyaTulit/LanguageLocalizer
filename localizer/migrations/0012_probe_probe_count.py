# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-08 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localizer', '0011_auto_20171008_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='probe',
            name='probe_count',
            field=models.IntegerField(default=83, verbose_name='Количество проб в условии'),
            preserve_default=False,
        ),
    ]
