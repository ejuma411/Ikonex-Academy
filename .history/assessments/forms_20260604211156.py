from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

from .models import Assessment


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'total_marks', 'term', 'year']

        help_texts = {
            'name': "e.g. CAT 1, Midterm, End Term",
            'term': "Enter term number (1, 2, or 3)",
            'year': "Enter valid year (e.g. 2024)"
        }

    # -------------------------
    # NAME VALIDATION
    # -------------------------
    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError("Assessment name is required.")

        name = name.strip().title()

        if len(name) < 3:
            raise ValidationError("Assessment name is too short.")

        if len(name) > 50:
            raise ValidationError("Assessment name is too long.")

        return name

    # -------------------------
    # TOTAL MARKS VALIDATION
    # -------------------------
    def clean_total_marks(self):
        marks = self.cleaned_data.get("total_marks")

        if marks is None:
            raise ValidationError("Total marks are required.")

        if marks <= 0:
            raise ValidationError("Total marks must be greater than 0.")

        if marks > 1000:
            raise ValidationError("Total marks is unrealistic.")

        return marks

    # -------------------------
    # TERM VALIDATION
    # -------------------------
    def clean_term(self):
        term = self.cleaned_data.get("term")

        if term not in [1, 2, 3]:
            raise ValidationError("Term must be 1, 2, or 3.")

        return term

    # -------------------------
    # YEAR VALIDATION
    # -------------------------
    def clean_year(self):
        year = self.cleaned_data.get("year")

        current_year = datetime.now().year

        if year < 2000 or year > current_year + 1:
            raise ValidationError(
                f"Year must be between 2000 and {current_year + 1}."
            )

        return year

    # -------------------------
    # GLOBAL VALIDATION
    # -------------------------
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        term = cleaned_data.get("term")
        year = cleaned_data.get("year")

        if name and term and year:
            exists = Assessment.objects.filter(
                name__iexact=name,
                term=term,
                year=year
            )

            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)

            if exists.exists():
                raise ValidationError(
                    "This assessment already exists for this term and year."
                )

        return cleaned_data