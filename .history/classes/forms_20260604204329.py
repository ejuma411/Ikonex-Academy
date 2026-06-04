import re
from django import forms
from .models import ClassStream


class ClassStreamForm(forms.ModelForm):
    class Meta:
        model = ClassStream
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Class name is required.")

        name = name.strip().title()

        # strict format: Form 1A, Form 2B, etc.
        pattern = r'^Form\s[1-9][A-Z]$'

        if not re.match(pattern, name):
            raise forms.ValidationError(
                "Invalid format. Use format like 'Form 1A', 'Form 2B', etc."
            )

        # prevent duplicates
        if ClassStream.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This class already exists.")

        return name