from django.db import models


class Subject(models.Model):
    code_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code_name


class Response(models.Model):
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    response_sound = models.FileField(upload_to='responses/')
