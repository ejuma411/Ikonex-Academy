from django.shortcuts import render
from students.models import Student
from classes.models import ClassStream
from subjects.models import Subject
from assessments.models import Assessment
from accounts.decorators import staff_required


@staff_required
def dashboard(request):
    context = {
        "students_count": Student.objects.count(),
        "classes_count": ClassStream.objects.count(),
        "subjects_count": Subject.objects.count(),
        "assessments_count": Assessment.objects.count(),
    }
    return render(request, "dashboard/index.html", context)
