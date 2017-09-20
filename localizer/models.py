import csv

from django.db import models
import uuid
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator


def create_control_condition_sequence():
    return 'test'


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

    @classmethod
    def get_subject_by_cookie(cls, request):
        unique_id = request.COOKIES.get(Subject.COOKIE_NAME)
        return Subject.objects.get(unique_id=unique_id)


class Probe(models.Model):
    probe_text = models.CharField(max_length=200)
    control_condition = models.CharField(max_length=200)
    probe_number = models.IntegerField("Порядковый номер предложения")
    date_added = models.DateTimeField(auto_now=True)

    @classmethod
    def add_from_file(cls, csv_file_name, control_condition):
        file_path = 'localizer/static/localizer/csv/{}.csv'.format(csv_file_name)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',')
            for row in file_reader:
                assert(len(row) == 1)
                probe = cls(probe_text=row[0], control_condition=control_condition,
                            probe_number=file_reader.line_num)
                probe.save()

    def __str__(self):
        return self.probe_text


class Response(models.Model):
    response_sound = models.FileField(upload_to='responses/')


class Answer(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    probe = models.ForeignKey(Probe, on_delete=models.PROTECT)
    response_sound_file_path = models.FilePathField()
    dt_recorded = models.DateTimeField(auto_now=True)

    def __str___(self):
        code_name = self.subject.code_name
        probe_text = self.probe.probe_text
        return "{}'s response to '{}'".format(code_name, probe_text)

    @staticmethod
    def get_next_probe(subject):
        answers = Answer.objects.filter(subject=subject)
        if not answers:
            next_probe_number = 1
        else:
            probe_numbers = [answer.probe.probe_number for answer in answers]
            next_probe_number = max(probe_numbers) + 1
        try:
            probe = Probe.objects.get(probe_number=next_probe_number)
            return probe
        except ObjectDoesNotExist:
            return None