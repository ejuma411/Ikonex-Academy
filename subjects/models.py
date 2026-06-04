from django.core.exceptions import ValidationError
from django.db import models
from classes.models import ClassStream

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def clean(self):
        self.code = (self.code or "").strip().upper()
        self.name = (self.name or "").strip()

        errors = {}
        if not self.code:
            errors["code"] = "Subject code is required."
        if not self.name:
            errors["name"] = "Subject name is required."
        if self.code and Subject.objects.exclude(pk=self.pk).filter(code__iexact=self.code).exists():
            errors["code"] = "A subject with this code already exists."
        if self.name and Subject.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            errors["name"] = "A subject with this name already exists."

        if errors:
            raise ValidationError(errors)


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
                  "class_stream",
                  "subject"
               ],
               name="unique_class_subject"
         )
      ]

    def __str__(self):
        return f"{self.class_stream} - {self.subject}"

    def clean(self):
        errors = {}
        if not self.class_stream_id:
            errors["class_stream"] = "Class stream is required."
        if not self.subject_id:
            errors["subject"] = "Subject is required."
        if self.class_stream_id and self.subject_id:
            duplicate = ClassSubject.objects.exclude(pk=self.pk).filter(
                class_stream=self.class_stream,
                subject=self.subject,
            )
            if duplicate.exists():
                errors["subject"] = "This subject is already assigned to the selected class stream."

        if errors:
            raise ValidationError(errors)
