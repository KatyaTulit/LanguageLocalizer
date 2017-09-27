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

    url(r'error_unknown_subject/$', views.unknown_subject, name='error_unknown_subject'),
    url(r'restart/$', views.restart, name='restart'),
    url(r'resume/$', views.resume, name='resume'),

    url(r'^$', views.file_choice, name='file_choice'),
    url(r'recorderjs_test/', views.recorderjs_test, name="recorderjs_test"),
]