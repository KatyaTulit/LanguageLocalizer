from django.conf.urls import url

from . import views

app_name = 'localizer'
urlpatterns = [
    url(r'^$', views.file_choice, name='file_choice'),
]