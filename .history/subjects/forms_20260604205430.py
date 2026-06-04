from django import forms
from .models import Subject, ClassSubject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name']


class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = ['class_stream', 'subject']