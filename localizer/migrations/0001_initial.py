# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-15 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_sound', models.FileField(upload_to='responses/')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_name', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizer.Subject'),
        ),
    ]