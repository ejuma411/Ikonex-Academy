from django.contrib import admin
from .models import ClassStream

@admin.register(ClassStream)
class ClassStreamAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_count']
    search_fields = ['name']
    list_filter = ['name']
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'