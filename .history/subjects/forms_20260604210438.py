from django import forms
from .models import Subject, ClassSubject
import re


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name']

        help_texts = {
            'code': "Subject code format: MATH, ENG, KISW (uppercase letters only)",
            'name': "Subject name: Mathematics, English, Kiswahili"
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')

        if not code:
            raise forms.ValidationError("Subject code is required.")

        code = code.strip().upper()

        # Only letters, 2–10 chars
        if not re.match(r'^[A-Z]{2,10}$', code):
            raise forms.ValidationError(
                "Invalid code. Use uppercase letters only (e.g. MATH, ENG)."
            )

        if Subject.objects.filter(code__iexact=code).exists():
            raise forms.ValidationError("This subject code already exists.")

        return code

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Subject name is required.")

        name = name.strip().title()

        if len(name) < 3:
            raise forms.ValidationError("Subject name is too short.")

        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError(
                "Subject name must contain letters only."
            )

        if Subject.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This subject already exists.")

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