from django import forms
from .models import Student
import re


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admission_no', 'first_name', 'last_name', 'class_stream']

        help_texts = {
            'admission_no': "Format: ADM001, ADM002, etc.",
            'first_name': "Enter student's first name (e.g. John)",
            'last_name': "Enter student's last name (e.g. Kamau)",
            'class_stream': "Select class like 'Form 1A', 'Form 2B', etc."
        }

    # ---------------------------
    # ADMISSION NUMBER VALIDATION
    # ---------------------------
    def clean_admission_no(self):
        admission_no = self.cleaned_data.get('admission_no')

        if not admission_no:
            raise forms.ValidationError("Admission number is required.")

        admission_no = admission_no.strip().upper()

        # Format: ADM001, ADM123 etc.
        pattern = r'^ADM\d{3,5}$'

        if not re.match(pattern, admission_no):
            raise forms.ValidationError(
                "Invalid format. Use ADM001, ADM002, etc."
            )

        if Student.objects.filter(admission_no__iexact=admission_no).exists():
            raise forms.ValidationError("This admission number already exists.")

        return admission_no

    # ---------------------------
    # FIRST NAME VALIDATION
    # ---------------------------
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise forms.ValidationError("First name is required.")

        first_name = first_name.strip().title()

        if len(first_name) < 2:
            raise forms.ValidationError("First name is too short.")

        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")

        return first_name

    # ---------------------------
    # LAST NAME VALIDATION
    # ---------------------------
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise forms.ValidationError("Last name is required.")

        last_name = last_name.strip().title()

        if len(last_name) < 2:
            raise forms.ValidationError("Last name is too short.")

        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")

        return last_name