from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Max

from .forms import UploadFileForm
from .models import Probe, Subject, Answer

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
    subject = Subject.objects.get(code_name='test')
    probe = Answer.get_next_probe(subject)
    if probe:
        return render(request, 'localizer/probe.html',
                      {'probe_text': probe.probe_text})
    else:
        return HttpResponse("Вы ответили на все вопросы. Спасибо вам большое.")

def upload_probe(request):
    if request.method == 'POST':
        subject = Subject.objects.get(code_name='test')
        probe = Answer.get_next_probe(subject)

        file_path = "responses/recording{}.ogg".format(probe.probe_number)
        with open(file_path, "wb") as f:
            f.write(request.body)

        answer = Answer(subject=subject, probe=probe,
                        response_sound_file_path=file_path)
        answer.save()

        # Redirect will be handled by js so we will send the URL in the body
        return HttpResponse(reverse('localizer:probe'))
    else:
        return HttpResponse("View should only be requested with POST")
