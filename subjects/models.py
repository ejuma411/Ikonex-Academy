from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from classes.models import ClassStream

User = get_user_model()


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ClassSubject(models.Model):
    class_stream = models.ForeignKey(
        ClassStream,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_assignments'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["class_stream", "subject"],
                name="unique_class_subject"
            )
        ]
        ordering = ['class_stream__name', 'subject__name']

    def __str__(self):
        return f"{self.class_stream.name} - {self.subject.name}"

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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TeacherSubjectAssignment(models.Model):
    """Assign a teacher to teach a specific subject in a specific class"""
    class_subject = models.ForeignKey(
        ClassSubject, 
        on_delete=models.CASCADE, 
        related_name='teacher_assignments'
    )
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='subject_assignments',
        limit_choices_to={'role': 'teacher'}
    )
    academic_year = models.CharField(max_length=9)  # e.g., "2024/2025"
    is_active = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_subjects'
    )
    assigned_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['class_subject', 'teacher', 'academic_year']
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.class_subject} - {self.teacher.get_full_name()} ({self.academic_year})"

    def clean(self):
        errors = {}
        if not self.class_subject_id:
            errors["class_subject"] = "Class subject is required."
        if not self.teacher_id:
            errors["teacher"] = "Teacher is required."
        if not self.academic_year:
            errors["academic_year"] = "Academic year is required."
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)