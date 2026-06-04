from django import forms
from .models import ClassStream
from django import forms
from .models import ClassSubject

import re


class ClassStreamForm(forms.ModelForm):
    class Meta:
        model = ClassStream
        fields = ['name']
        help_texts = {
            'name': "Enter class in format like 'Form 1A', 'Form 2B', etc."
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Class name is required.")

        name = name.strip().title()

        # ✅ enforce format: Form 1A, Form 2B, etc.
        pattern = r'^Form\s\d+[A-Z]$'

        if not re.match(pattern, name):
            raise forms.ValidationError(
                "Invalid format. Use 'Form 1A', 'Form 2B', etc."
            )

        # prevent duplicates
        if ClassStream.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This class already exists.")

        return name
    

class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = ['class_stream', 'subject']

        help_texts = {
            'class_stream': "Select class (e.g. Form 1A)",
            'subject': "Select subject (e.g. Mathematics)"
        }

    def clean(self):
        cleaned_data = super().clean()
        class_stream = cleaned_data.get('class_stream')
        subject = cleaned_data.get('subject')

        if class_stream and subject:
            if ClassSubject.objects.filter(
                class_stream=class_stream,
                subject=subject
            ).exists():
                raise forms.ValidationError(
                    "This subject is already assigned to this class."
                )

        return cleaned_data