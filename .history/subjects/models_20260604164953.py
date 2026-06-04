from django.db import models
from classes.models import ClassStream

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassSubject(models.Model):
    class_stream = models.ForeignKey(
        ClassStream,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
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