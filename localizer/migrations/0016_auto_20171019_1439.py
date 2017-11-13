# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localizer', '0015_auto_20171018_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='education',
            field=models.CharField(choices=[('Higher', 'Высшее'), ('Student', 'Получаю высшее (студент)'), ('College', 'Среднее профессиональное (техникум, колледж)'), ('HighSchool', 'Полное среднее (11 классов)'), ('NineClasses', 'Неполное среднее (9 классов)')], max_length=20),
        ),
    ]