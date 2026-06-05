from django.contrib import admin
from .models import Subject, ClassSubject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['class_stream', 'subject']
    list_filter = ['class_stream', 'subject']
    search_fields = ['class_stream__name', 'subject__name']