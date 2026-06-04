from django.contrib import admin
from .models import ClassStream


@admin.register(ClassStream)
class ClassStreamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
