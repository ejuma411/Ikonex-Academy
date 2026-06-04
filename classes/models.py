import re

from django.core.exceptions import ValidationError
from django.db import models

class ClassStream(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        self.name = (self.name or "").strip()
        if not self.name:
            raise ValidationError({"name": "Class stream name is required."})
        if ClassStream.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError({"name": "A class stream with this name already exists."})
