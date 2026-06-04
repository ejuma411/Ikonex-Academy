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

        name = name.strip()

        if len(name) < 2:
            raise forms.ValidationError("Class name is too short.")

        if len(name) > 50:
            raise forms.ValidationError("Class name is too long (max 50 characters).")

        # prevent duplicates (case-insensitive)
        if ClassStream.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This class already exists.")

        return name