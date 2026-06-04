from django import forms
from django.core.exceptions import ValidationError

from .models import Assessment, GradeScale, Score
from subjects.models import ClassSubject


# ==================================================
# ASSESSMENT FORM
# ==================================================
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'total_marks', 'term', 'year']


# ==================================================
# SCORE FORM
# ==================================================
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['student', 'subject', 'assessment', 'marks']

    def clean(self):
        cleaned_data = super().clean()

        student = cleaned_data.get("student")
        subject = cleaned_data.get("subject")
        assessment = cleaned_data.get("assessment")
        marks = cleaned_data.get("marks")

        # -----------------------------------------
        # 1. Ensure subject belongs to class stream
        # -----------------------------------------
        if student and subject:
            valid = ClassSubject.objects.filter(
                class_stream=student.class_stream,
                subject=subject
            ).exists()

            if not valid:
                self.add_error(
                    "subject",
                    "This subject is not assigned to the student's class stream."
                )

        # -----------------------------------------
        # 2. Validate marks range
        # -----------------------------------------
        if assessment is not None and marks is not None:
            if marks < 0:
                self.add_error("marks", "Marks cannot be negative.")

            if marks > assessment.total_marks:
                self.add_error(
                    "marks",
                    f"Marks cannot exceed {assessment.total_marks}."
                )

        # -----------------------------------------
        # 3. Prevent duplicate score entry
        # -----------------------------------------
        if student and subject and assessment:
            qs = Score.objects.filter(
                student=student,
                subject=subject,
                assessment=assessment
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error(
                    None,
                    "Score already exists for this student, subject, and assessment."
                )

        return cleaned_data


# ==================================================
# GRADE SCALE FORM
# ==================================================
class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = ["grade", "min_mark", "max_mark"]

    def clean(self):
        cleaned_data = super().clean()

        grade = cleaned_data.get("grade")
        min_mark = cleaned_data.get("min_mark")
        max_mark = cleaned_data.get("max_mark")

        # -----------------------------------------
        # 1. Validate range logic
        # -----------------------------------------
        if min_mark is not None and max_mark is not None:
            if min_mark > max_mark:
                self.add_error(
                    "min_mark",
                    "Minimum mark cannot be greater than maximum mark."
                )

        # -----------------------------------------
        # 2. Prevent duplicate grade
        # -----------------------------------------
        if grade:
            qs = GradeScale.objects.filter(grade__iexact=grade)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error("grade", "This grade already exists.")

        # -----------------------------------------
        # 3. Prevent overlapping grade ranges
        # -----------------------------------------
        if min_mark is not None and max_mark is not None:
            overlap = GradeScale.objects.all()

            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)

            overlap = overlap.filter(
                min_mark__lte=max_mark,
                max_mark__gte=min_mark
            )

            if overlap.exists():
                self.add_error(
                    None,
                    "Grade range overlaps with an existing grade scale."
                )

        return cleaned_data