from django.shortcuts import render, redirect, get_object_or_404
from .models import Assessment, Score, Student
from .forms import AssessmentForm, ScoreForm


# -------------------
# ASSESSMENTS
# -------------------

def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'assessments/list.html', {'assessments': assessments})


def assessment_detail(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    scores = Score.objects.filter(assessment=assessment)
    return render(request, 'assessments/detail.html', {
        'assessment': assessment,
        'scores': scores
    })


def assessment_create(request):
    form = AssessmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('assessment_list')
    return render(request, 'assessments/create.html', {'form': form})


def assessment_update(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    form = AssessmentForm(request.POST or None, instance=assessment)
    if form.is_valid():
        form.save()
        return redirect('assessment_list')
    return render(request, 'assessments/update.html', {'form': form})


def assessment_delete(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    if request.method == "POST":
        assessment.delete()
        return redirect('assessment_list')
    return render(request, 'assessments/delete.html', {'assessment': assessment})


# -------------------
# SCORE ENTRY
# -------------------

def score_list(request):
    scores = Score.objects.select_related('student', 'subject', 'assessment')
    return render(request, 'assessments/scores/list.html', {'scores': scores})


def score_create(request):
    form = ScoreForm(request.POST or None)

    if form.is_valid():
        try:
            form.save()
            return redirect('score_list')
        except:
            form.add_error(None, "Score already exists for this student, subject, and assessment.")

    return render(request, 'assessments/scores/create.html', {'form': form})
 
def student_result_view(request, pk):
    student = get_object_or_404(Student, pk=pk)

    scores = Score.objects.filter(student=student).select_related(
        'assessment',
        'subject'
    )

    return render(request, 'assessments/results/student_result.html', {
        'student': student,
        'scores': scores
    })
    