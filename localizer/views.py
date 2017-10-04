from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UploadFileForm, SubjectQuestionnaireForm
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


def upload_probe(request):
    if request.method == 'POST':
        subject = Subject.get_subject_by_cookie(request)
        probe = Answer.get_next_probe(subject)
        file_path = Answer.save_sound_file(sound_content=request.body, subject=subject, probe=probe)
        answer = Answer(subject=subject, probe=probe, response_sound_file_path=file_path)
        answer.save()

        # Redirect will be handled by js so we will send the URL in the body
        return HttpResponse(reverse('localizer:task'))
    else:
        return HttpResponseRedirect(reverse('localizer:task'))


def welcome(request):
    subject = Subject.get_subject_by_cookie(request)
    if subject is None:
        return render(request, 'localizer/welcome.html')
    else:
        return render(request, 'localizer/error_same_subject.html')


def soundtest(request):
    subject = Subject.get_subject_by_cookie(request)
    if subject is None:
        return render(request, 'localizer/soundtest.html')
    else:
        return render(request, 'localizer/error_same_subject.html')


def questionnaire(request):
    subject = Subject.get_subject_by_cookie(request)
    if subject is None:
        if request.method == 'POST':
            form = SubjectQuestionnaireForm(request.POST, request.FILES)
            if form.is_valid():
                subject = form.save()
                subject.make_dirs()
                response = HttpResponseRedirect(reverse('localizer:instructions'))
                response.set_cookie(Subject.COOKIE_NAME, subject.unique_id)
                return response
        else:
            form = SubjectQuestionnaireForm()
        return render(request, 'localizer/questionnaire.html', {'form': form})
    else:
        return render(request, 'localizer/error_same_subject.html')


def unknown_subject(request):
    return render(request, 'localizer/error_unknown_subject.html')


def restart(request):
    response = HttpResponseRedirect(reverse('localizer:welcome'))
    response.delete_cookie(Subject.COOKIE_NAME)
    return response


def resume(request):
    response = HttpResponseRedirect(reverse('localizer:instructions'))
    return response


def task(request):
    subject = Subject.get_subject_by_cookie(request)
    if subject is None:
        return restart(request)
    else:
        probe = Answer.get_next_probe(subject)

        if probe is not None:
            return render(request, 'localizer/probe.html',
                          {'probe_text': probe.probe_text})
        else:
            return render(request, 'localizer/end.html')


def instructions(request):
    subject = Subject.get_subject_by_cookie(request)
    if subject is None:
        return restart(request)
    else:
        return render(request, 'localizer/instructions.html')