from django import forms
from .models import Response


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['response_sound']

