from django import forms
from django.core.exceptions import ValidationError
from .models import Assessment, GradeScale, Score
from subjects.models import ClassSubject


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'total_marks', 'term', 'year']


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

        if student and subject:
            if not ClassSubject.objects.filter(
                class_stream=student.class_stream,
                subject=subject,
            ).exists():
                raise ValidationError(
                    "This subject is not assigned to the student's class stream."
                )

        if assessment and marks is not None:
            if marks < 0:
                raise ValidationError("Marks cannot be negative.")
            if marks > assessment.total_marks:
                raise ValidationError(
                    f"Marks cannot exceed the assessment total of {assessment.total_marks}."
                )

        if student and subject and assessment:
            qs = Score.objects.filter(
                student=student,
                subject=subject,
                assessment=assessment,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    "Score already exists for this student, subject, and assessment."
                )

        return cleaned_data


class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = ["grade", "min_mark", "max_mark"]

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get("grade")
        min_mark = cleaned_data.get("min_mark")
        max_mark = cleaned_data.get("max_mark")

        if min_mark is not None and max_mark is not None and min_mark > max_mark:
            raise ValidationError("Minimum mark cannot be greater than maximum mark.")

        if grade:
            qs = GradeScale.objects.filter(grade__iexact=grade)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Grade already exists.")

        if min_mark is not None and max_mark is not None:
            overlap = GradeScale.objects.all()
            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)
            overlap = overlap.filter(
                min_mark__lte=max_mark,
                max_mark__gte=min_mark,
            )
            if overlap.exists():
                raise ValidationError("Grade range overlaps with an existing scale.")

        return cleaned_data
