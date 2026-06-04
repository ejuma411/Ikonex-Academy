from django.core.exceptions import ValidationError
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

    def clean(self):
        self.admission_no = (self.admission_no or "").strip().upper()
        self.first_name = (self.first_name or "").strip()
        self.last_name = (self.last_name or "").strip()

        errors = {}
        if not self.admission_no:
            errors["admission_no"] = "Admission number is required."
        if not self.first_name:
            errors["first_name"] = "First name is required."
        if not self.last_name:
            errors["last_name"] = "Last name is required."
        if not self.class_stream_id:
            errors["class_stream"] = "Class stream is required."

        if self.admission_no and Student.objects.exclude(pk=self.pk).filter(admission_no__iexact=self.admission_no).exists():
            errors["admission_no"] = "A student with this admission number already exists."

        if errors:
            raise ValidationError(errors)
