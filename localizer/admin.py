from django.contrib import admin

from .models import Subject, Answer


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code_name', 'probe_control_conditions', 'unique_id', 'finished')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('probe', 'subject', 'response_sound_file_path')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Answer, AnswerAdmin)