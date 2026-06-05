from django.db import models

from students.models import Student
from subjects.models import Subject



TERM_CHOICES = [
    ("1", "Term 1"),
    ("2", "Term 2"),
    ("3", "Term 3"),
]


class Assessment(models.Model):
    name = models.CharField(max_length=50)

    total_marks = models.IntegerField(default=100)

    term = models.CharField(
        max_length=1,
        choices=TERM_CHOICES
    )

    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Term {self.term} ({self.year})"


class GradeScale(models.Model):
    GRADE_CHOICES = (
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
    )
    
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, unique=True)
    min_mark = models.PositiveSmallIntegerField(verbose_name="Minimum Mark")
    max_mark = models.PositiveSmallIntegerField(verbose_name="Maximum Mark")
    
    class Meta:
        ordering = ['-max_mark']
        verbose_name = "Grade Scale"
        verbose_name_plural = "Grade Scales"
    
    def __str__(self):
        return f"{self.grade} ({self.min_mark}-{self.max_mark})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.min_mark < 0 or self.min_mark > 100:
            raise ValidationError({'min_mark': "Minimum mark must be between 0 and 100."})
        
        if self.max_mark < 0 or self.max_mark > 100:
            raise ValidationError({'max_mark': "Maximum mark must be between 0 and 100."})
        
        if self.min_mark >= self.max_mark:
            raise ValidationError("Minimum mark must be less than maximum mark.")
        
        # Check for overlapping ranges
        overlapping = GradeScale.objects.exclude(pk=self.pk).filter(
            min_mark__lte=self.max_mark,
            max_mark__gte=self.min_mark
        )
        if overlapping.exists():
            raise ValidationError(f"Range overlaps with grade '{overlapping.first().grade}'")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Score(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE
    )

    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    class Meta:
      constraints = [
         models.UniqueConstraint(
               fields=[
                  "student",
                  "subject",
                  "assessment"
               ],
               name="unique_student_subject_assessment"
         )
      ]

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.assessment}"
