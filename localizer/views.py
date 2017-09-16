from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UploadFileForm
from .models import Probe

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
    probe = get_object_or_404(Probe, probe_number=1)
    return render(request, 'localizer/probe.html',
                  {'probe_text': probe.probe_text})

def upload_probe(request):
    if request.method == 'POST':
        with open("responses/recording2.ogg", "wb") as f:
            f.write(request.body)

    else:
        return HttpResponse("View should only be requested with POST")
