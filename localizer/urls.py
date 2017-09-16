from django.conf.urls import url

from . import views

app_name = 'localizer'
urlpatterns = [
    url(r'^$', views.file_choice, name='file_choice'),
    url(r'recorderjs_test/', views.recorderjs_test, name="recorderjs_test"),
    url(r'probe/$', views.probe, name='probe'),
    url(r'probe/upload/$', views.upload_probe, name='upload_probe'),

]