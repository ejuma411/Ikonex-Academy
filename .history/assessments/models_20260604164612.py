from django.db import models

from students.models import Student
from subjects.models import Subject


class Assessment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name