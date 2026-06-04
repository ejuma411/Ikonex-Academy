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

    class Assessment(models.Model):


    term = models.CharField(
            max_length=1,
            choices=TERM_CHOICES
    )


    year = models.IntegerField()

    def __str__(self):
        term = f" {self.term}" if self.term else ""
        return f"{self.name}{term} ({self.year})"


class GradeScale(models.Model):
    grade = models.CharField(max_length=2, unique=True)

    min_mark = models.IntegerField()
    max_mark = models.IntegerField()

    def __str__(self):
        return self.grade

    class Meta:
        ordering = ("min_mark",)


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
