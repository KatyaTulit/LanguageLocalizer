import csv
import os

import pandas as pd
from django.db import models
import uuid
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator


def create_control_condition_sequence():
    return 'syl'


class Subject(models.Model):
    COOKIE_NAME = 'subject_id'

    code_name = models.CharField(max_length=15)
    date_added = models.DateTimeField(auto_now=True)
    probe_control_conditions = models.CharField(max_length=200,
                                                default=create_control_condition_sequence)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    unique_id = models.UUIDField(default=uuid.uuid4,
                                 editable=False)

    gender = models.CharField(
        max_length=10,
        choices=(
            ('female', 'Женщина'), ('male', 'Мужчина'), ('other', 'Иное')
        )
    )

    languages = models.CharField(max_length=30, default='нет')

    DIPLOMA = 'Higher'
    STUDENT = 'Student'
    HIGHSCHOOL = 'HighSchool'
    NINECLASSES = 'NineClasses'
    EDUCATION_CHOICES = (
        (DIPLOMA, 'Высшее'),
        (STUDENT, 'Получаю высшее (студент)'),
        (HIGHSCHOOL, 'Полное среднее, среднее специальное'),
        (NINECLASSES, 'Неполное среднее'),
    )
    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
    )

    def __str__(self):
        return self.code_name

    def get_next_probe(self):
        answers = Answer.objects.filter(subject=self)
        if not answers:
            next_probe_number = 1
        else:
            probe_numbers = [answer.probe.probe_number for answer in answers]
            next_probe_number = max(probe_numbers) + 1

        try:
            probe = Probe.objects.get(probe_number=next_probe_number, control_condition=self.probe_control_conditions)
            return probe
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_subject_by_cookie(cls, request):
        unique_id = request.COOKIES.get(Subject.COOKIE_NAME)
        try:
            return Subject.objects.get(unique_id=unique_id)
        except ObjectDoesNotExist:
            return None

    def answer_dir(self):
        subject_dir = self.code_name or str(self.unique_id)
        return os.path.join(Answer.BASE_DIR, subject_dir)

    def make_dirs(self):
        control_conditions = self.probe_control_conditions.split(',')
        for control_condition in control_conditions:
            dir = self.answer_dir(control_condition)
            if not os.path.exists(dir):
                os.makedirs(dir)


class Probe(models.Model):
    probe_text = models.CharField(max_length=200)
    control_condition = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)
    block_number = models.IntegerField("Номер блока")
    probe_number = models.IntegerField("Порядковый номер предложения")
    last_in_block = models.BooleanField("Проба является последней в блоке")

    @classmethod
    def add_from_file(cls, csv_file_name):
        file_path = 'localizer/static/localizer/csv/{}.csv'.format(csv_file_name)
        df = pd.read_csv(file_path, header=0, sep=";")
        for i, r in df.iterrows():
            probe = cls(probe_text=r['Sentence'], control_condition=r['Condition'],
                        block_number=r['block_number'], probe_number=r['probe_number'],
                        last_in_block=r['last_in_block'])
            probe.save()

    def __str__(self):
        return self.probe_text


class Response(models.Model):
    response_sound = models.FileField(upload_to='responses/')


class Answer(models.Model):
    BASE_DIR = 'answers/'

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    probe = models.ForeignKey(Probe, on_delete=models.PROTECT)
    response_sound_file_path = models.FilePathField()
    dt_recorded = models.DateTimeField(auto_now=True)

    def __str___(self):
        code_name = self.subject.code_name
        probe_text = self.probe.probe_text
        return "{}'s response to '{}'".format(code_name, probe_text)

    @classmethod
    def save_sound_file(cls, sound_content, subject, probe):
        file_path = os.path.join(subject.answer_dir(),
                                 "probe_{}.ogg".format(probe.probe_number))
        with open(file_path, "wb") as f:
            f.write(sound_content)
        return file_path
