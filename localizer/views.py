import os
import json

import boto3
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings

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
        probe = subject.get_next_probe()
        file_path = Answer.save_sound_file(sound_content=request.body, subject=subject, probe=probe)
        answer = Answer(subject=subject, probe=probe, response_sound_file_path=file_path)
        answer.save()

        if not probe.last_in_block:
            url = reverse('localizer:task')
        else:
            if probe.block_number == 0:
                url = reverse('localizer:training_finished')
            else:
                url = reverse('localizer:task_break')

        # Redirect will be handled by js so we will send the URL in the body
        return HttpResponse(url)

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
                subject.choose_condition()
                subject.make_dirs()
                response = HttpResponseRedirect(reverse('localizer:instructions'))
                response.set_cookie(Subject.COOKIE_NAME, subject.unique_id, max_age=2*24*60*60)
                return response
        else:
            form = SubjectQuestionnaireForm()
        return render(request, 'localizer/questionnaire.html', {'form': form})
    else:
        return render(request, 'localizer/error_same_subject.html')

def sound_problems(request):
    redirected_from = request.COOKIES.get('redirected_from')
    response = render(request, 'localizer/sound_problems.html', {'redirected_from': redirected_from})
    response.delete_cookie('redirected_from')
    return response

def upload_problems(request):
    return render(request, 'localizer/upload_problems.html')

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
        if not subject.last_answer_successfully_uploaded():
            return HttpResponseRedirect(reverse('localizer:upload_problems'))

        probe = subject.get_next_probe()

        if probe is not None:
            percentage_complete = round(probe.probe_number / probe.probe_count * 100)
            return render(request, 'localizer/probe.html',
                          {'probe_text': probe.probe_text,
                           'percentage_complete': percentage_complete})
        else:
            return render(request, 'localizer/end.html')


def sign_s3(request):
    if request.method == 'POST':

        subject = Subject.get_subject_by_cookie(request)
        probe = subject.get_next_probe()
        file_path = Answer.get_file_url(subject=subject, probe=probe)

        S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME

        s3_file_path = 'https://{}.s3-eu-west-1.amazonaws.com/{}'.format(S3_BUCKET, file_path)
        s3_file_path = 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_path)

        answer = Answer(subject=subject, probe=probe, response_sound_file_path=s3_file_path)
        answer.save()

        if not probe.last_in_block:
            redirect_url = reverse('localizer:task')
        else:
            if probe.block_number == 0:
                redirect_url = reverse('localizer:training_finished')
            else:
                redirect_url = reverse('localizer:task_break')

        s3 = boto3.client('s3')

        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_path,
            Fields={"acl": "private", "Content-Type": "audio/ogg"},
            Conditions=[
                {"acl": "private"},
                {"Content-Type": "audio/ogg"}
            ],
            ExpiresIn=3600
        )

        # presigned_post['url'] = 'https://languagelocalizer2.s3.amazonaws.com/'

        data = json.dumps({
            'data': presigned_post,
            'url': s3_file_path,
            'redirect_url': redirect_url
        })
        return HttpResponse(data, content_type='application/json')

    else:
        return HttpResponseRedirect(reverse('localizer:task'))


def instructions(request):
    subject = Subject.get_subject_by_cookie(request)
    if subject is None:
        return restart(request)
    else:
        return render(request, 'localizer/instructions.html')


def training_finished(request):
    return render(request, 'localizer/training_finished.html')

def task_break(request):
    return render(request, 'localizer/task_break.html')