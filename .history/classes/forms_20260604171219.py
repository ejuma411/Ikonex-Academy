from django import forms
from .models import ClassStream


class ClassStreamForm(forms.ModelForm):
    class Meta:
        model = ClassStream
        fields = ['name']