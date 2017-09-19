from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Response, Subject


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['response_sound']


class SubjectQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['age', 'gender', 'education']
        labels = {'age': 'Возраст', 'gender': 'Пол', 'education': 'Образование'}
        error_messages = {
            'age': {
                'max_value': "Пожалуйста, введите значение от 1 до 100",
                'min_value': "Пожалуйста, введите значение от 1 до 100"
            }
        }

