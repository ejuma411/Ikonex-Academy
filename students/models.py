from django.core.exceptions import ValidationError
from django.db import models
from classes.models import ClassStream
from datetime import date


class Student(models.Model):
    # blank=True allows the pre-save empty state before auto-generation (Issue #2)
    admission_no = models.CharField(max_length=20, unique=True, blank=True)
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

    def generate_admission_no(self):
        """Auto-generate admission number in format ADM/YYYY/NNNN (Issue #2)."""
        year = date.today().year
        prefix = f"ADM/{year}/"

        last_student = Student.objects.filter(
            admission_no__startswith=prefix
        ).order_by('-admission_no').first()

        if last_student and last_student.admission_no:
            try:
                last_num = int(last_student.admission_no.replace(prefix, ''))
                new_num = last_num + 1
            except ValueError:
                new_num = 1
        else:
            new_num = 1

        return f"{prefix}{new_num:04d}"

    def save(self, *args, **kwargs):
        if not self.admission_no:
            self.admission_no = self.generate_admission_no()
        super().save(*args, **kwargs)

    def clean(self):
        self.first_name = (self.first_name or "").strip()
        self.last_name = (self.last_name or "").strip()

        errors = {}
        if not self.first_name:
            errors["first_name"] = "First name is required."
        if not self.last_name:
            errors["last_name"] = "Last name is required."
        if not self.class_stream_id:
            errors["class_stream"] = "Class stream is required."

        if errors:
            raise ValidationError(errors)
