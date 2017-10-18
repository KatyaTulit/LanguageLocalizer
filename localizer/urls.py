from django.conf.urls import url

from . import views

app_name = 'localizer'
urlpatterns = [
    url(r'welcome/$', views.welcome, name='welcome'),
    url(r'soundtest/$', views.soundtest, name='soundtest'),
    url(r'questionnaire/$', views.questionnaire, name='questionnaire'),

    url(r'instructions/$', views.instructions, name='instructions'),
    url(r'task/$', views.task, name='task'),
    url(r'task/upload/$', views.upload_probe, name='upload_probe'),
    url(r'task/sign_s3/$', views.sign_s3, name='sign_s3'),

    url(r'training_finished/$', views.training_finished, name='training_finished'),
    url(r'task_break/$', views.task_break, name='task_break'),

    url(r'error_unknown_subject/$', views.unknown_subject, name='error_unknown_subject'),
    url(r'sound_problems/$', views.sound_problems, name='sound_problems'),
    url(r'upload_problems/$', views.upload_problems, name='upload_problems'),
    url(r'restart/$', views.restart, name='restart'),
    url(r'resume/$', views.resume, name='resume'),

    url(r'^$', views.file_choice, name='file_choice'),
    url(r'recorderjs_test/', views.recorderjs_test, name="recorderjs_test"),
]