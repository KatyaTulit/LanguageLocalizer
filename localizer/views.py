from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UploadFileForm
from .models import Response

def file_choice(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('localizer:file_choice'))
    else:
        form = UploadFileForm()
    return render(request, 'localizer/upload.html', {'form': form})

def recorderjs_test(request):
    return render(request, 'localizer/waveRecorder.html')


def probe(request):
    form = UploadFileForm()
    return render(request, 'localizer/probe.html', {'form': form})

def upload_probe(request):
    if request.method == 'POST':
        with open("responses/recording2.ogg", "wb") as f:
            f.write(request.body)

        return HttpResponse("Sound uploaded")
    else:
        return HttpResponse("View should only be requested with POST")
