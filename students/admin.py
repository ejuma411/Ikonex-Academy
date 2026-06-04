from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_no", "first_name", "last_name", "class_stream")
    search_fields = ("admission_no", "first_name", "last_name")
    list_select_related = ("class_stream",)
