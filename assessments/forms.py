from django import forms
from django.core.exceptions import ValidationError
from .models import Assessment, GradeScale, Score
from subjects.models import ClassSubject
from django.utils import timezone

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'total_marks', 'term', 'year']

        help_texts = {
            "name": "e.g. CAT 1, Midterm, End Term",
            "term": "1, 2, or 3",
            "year": "e.g. Between 2022 and current year",
            "total_marks": "Must be between 1 and 100"
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError("Assessment name is required.")

        name = name.strip().title()

        if len(name) < 3:
            raise ValidationError("Name is too short.")

        return name

    def clean_term(self):
        term = self.cleaned_data.get("term")

        if str(term).strip() not in ["1", "2", "3"]:
            raise ValidationError("Term must be 1, 2, or 3.")

        return str(term).strip()

    def clean_year(self):
        year = self.cleaned_data.get("year")
        current_year = timezone.now().year
        
        if year is None:
            raise ValidationError("Year is required.")
        
        if year < 2022:
            raise ValidationError(f"Year cannot be earlier than 2020. Please enter a year from 2020 onwards.")
        
        if year > current_year:
            raise ValidationError(f"Year cannot be in the future. Please enter a year up to {current_year}.")
        
        return year

    def clean_total_marks(self):
        marks = self.cleaned_data.get("total_marks")

        if marks <= 0:
            raise ValidationError("Total marks must be greater than 0.")

        if marks > 100:
            raise ValidationError("Total marks is unrealistically high.")

        return marks


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
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'min_mark': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control', 'step': 1}),
            'max_mark': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control', 'step': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define grade choices - WITHOUT hardcoded ranges
        grade_choices = [
            ('A', 'A'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B', 'B'),
            ('B-', 'B-'),
            ('C+', 'C+'),
            ('C', 'C'),
            ('C-', 'C-'),
            ('D+', 'D+'),
            ('D', 'D'),
            ('D-', 'D-'),
            ('E', 'E'),
        ]
        self.fields['grade'].widget.choices = grade_choices
    
    def clean_grade(self):
        grade = self.cleaned_data.get("grade")
        valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
        
        if not grade:
            raise ValidationError("Grade is required.")
        
        if grade not in valid_grades:
            raise ValidationError(f"Invalid grade. Choose from: {', '.join(valid_grades)}")
        
        # Check for duplicate grade
        qs = GradeScale.objects.filter(grade__iexact=grade)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(f"Grade '{grade}' already exists.")
        
        return grade
    
    def clean_min_mark(self):
        min_mark = self.cleaned_data.get("min_mark")
        if min_mark is None:
            raise ValidationError("Minimum mark is required.")
        if min_mark < 0 or min_mark > 100:
            raise ValidationError("Minimum mark must be between 0 and 100.")
        return min_mark
    
    def clean_max_mark(self):
        max_mark = self.cleaned_data.get("max_mark")
        if max_mark is None:
            raise ValidationError("Maximum mark is required.")
        if max_mark < 0 or max_mark > 100:
            raise ValidationError("Maximum mark must be between 0 and 100.")
        return max_mark
    
    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get("grade")
        min_mark = cleaned_data.get("min_mark")
        max_mark = cleaned_data.get("max_mark")
        
        # Validate min < max
        if min_mark is not None and max_mark is not None:
            if min_mark >= max_mark:
                raise ValidationError("Minimum mark must be less than maximum mark.")
        
        # Check for overlapping ranges
        if min_mark is not None and max_mark is not None:
            overlap = GradeScale.objects.all()
            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)
            overlap = overlap.filter(
                min_mark__lte=max_mark,
                max_mark__gte=min_mark,
            )
            if overlap.exists():
                overlapping_grade = overlap.first()
                raise ValidationError(
                    f"Grade range overlaps with existing scale '{overlapping_grade.grade}' "
                    f"({overlapping_grade.min_mark}-{overlapping_grade.max_mark})."
                )
        
        return cleaned_data
