from django.contrib import admin
from .models import Assessment, GradeScale, Score


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("name", "term", "year", "total_marks")
    list_filter = ("year", "term")
    search_fields = ("name", "term")


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ("grade", "min_mark", "max_mark")
    ordering = ("-min_mark",)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "assessment", "marks")
    list_filter = ("assessment", "subject")
    search_fields = ("student__admission_no", "student__first_name", "student__last_name")
