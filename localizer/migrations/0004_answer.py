# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-16 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localizer', '0003_probe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_sound_file_path', models.FilePathField()),
                ('dt_recorded', models.DateTimeField(auto_now=True)),
                ('probe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localizer.Probe')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localizer.Subject')),
            ],
        ),
    ]
