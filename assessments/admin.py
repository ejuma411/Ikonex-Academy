from django.contrib import admin
from .models import Assessment, Score, GradeScale

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_marks', 'term', 'year']
    list_filter = ['term', 'year']
    search_fields = ['name']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'assessment', 'marks']
    list_filter = ['assessment', 'subject']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ['grade', 'min_mark', 'max_mark']
    list_editable = ['min_mark', 'max_mark']