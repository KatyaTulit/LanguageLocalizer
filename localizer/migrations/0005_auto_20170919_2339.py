# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 20:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localizer', '0004_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='age',
            field=models.IntegerField(default=99, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='education',
            field=models.CharField(choices=[('Higher', 'Высшее'), ('Student', 'Получаю высшее (студент)'), ('HighSchool', 'Полное среднее, среднее специальное'), ('NineClasses', 'Неполное среднее')], default='Higher', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='gender',
            field=models.CharField(choices=[('female', 'Женщина'), ('male', 'Мужчина'), ('other', 'Иное')], default='other', max_length=10),
            preserve_default=False,
        ),
    ]