from django.db import models
from classes.models import ClassStream

class Student(models.Model):
    admission_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class_stream = models.ForeignKey(
        ClassStream,
        on_delete=models.CASCADE,
        related_name="students"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"