import csv

from django.db import models
from django.templatetags.static import static


class Subject(models.Model):
    code_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code_name


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