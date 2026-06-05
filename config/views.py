import datetime
from django.shortcuts import render
from students.models import Student
from classes.models import ClassStream
from subjects.models import Subject
from assessments.models import Assessment
from accounts.decorators import staff_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@staff_required
def dashboard(request):
    context = {
        "students_count": Student.objects.count(),
        "classes_count": ClassStream.objects.count(),
        "subjects_count": Subject.objects.count(),
        "assessments_count": Assessment.objects.count(),
    }
    return render(request, "dashboard/index.html", context)



@login_required
@csrf_protect
def refresh_session(request):
    """Reset session timer"""
    request.session['last_activity'] = datetime.now().timestamp()
    return JsonResponse({'status': 'ok'})

from django.http import JsonResponse
from django.shortcuts import render


def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Ikonex Academy API is running',
        'environment': 'production'
    })


def home_view(request):
    return render(request, 'base/base.html')