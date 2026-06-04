from django.shortcuts import get_object_or_404, redirect, render

from assessments.forms import AssessmentForm, ScoreForm
from assessments.models import Assessment, Score
from assessments.results import class_ranking, class_subject_ranking, student_result
from classes.models import ClassStream
from students.models import Student


def assessment_list(request):
    assessments = Assessment.objects.all().order_by("-year", "term", "name")
    return render(request, "assessments/list.html", {"assessments": assessments})


def assessment_detail(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    scores = Score.objects.filter(assessment=assessment).select_related(
        "student",
        "subject",
    )
    return render(
        request,
        "assessments/detail.html",
        {
            "assessment": assessment,
            "scores": scores,
        },
    )


def assessment_create(request):
    form = AssessmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("assessment_list")
    return render(request, "assessments/create.html", {"form": form})


def assessment_update(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    form = AssessmentForm(request.POST or None, instance=assessment)
    if form.is_valid():
        form.save()
        return redirect("assessment_list")
    return render(request, "assessments/update.html", {"form": form, "assessment": assessment})


def assessment_delete(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    if request.method == "POST":
        assessment.delete()
        return redirect("assessment_list")
    return render(request, "assessments/delete.html", {"assessment": assessment})


def score_list(request):
    scores = Score.objects.select_related("student", "subject", "assessment").order_by(
        "-assessment__year",
        "assessment__name",
        "student__last_name",
        "student__first_name",
    )
    return render(request, "assessments/scores/list.html", {"scores": scores})


def score_detail(request, pk):
    score = get_object_or_404(
        Score.objects.select_related("student", "subject", "assessment"),
        pk=pk,
    )
    return render(request, "assessments/scores/detail.html", {"score": score})


def score_create(request):
    form = ScoreForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("score_list")
    return render(request, "assessments/scores/create.html", {"form": form})


def score_update(request, pk):
    score = get_object_or_404(Score, pk=pk)
    form = ScoreForm(request.POST or None, instance=score)
    if form.is_valid():
        form.save()
        return redirect("score_list")
    return render(request, "assessments/scores/update.html", {"form": form, "score": score})


def score_delete(request, pk):
    score = get_object_or_404(Score, pk=pk)
    if request.method == "POST":
        score.delete()
        return redirect("score_list")
    return render(request, "assessments/scores/delete.html", {"score": score})


def student_result_view(request, pk):
    student = get_object_or_404(Student.objects.select_related("class_stream"), pk=pk)
    result = student_result(student)
    class_summary = class_ranking(student.class_stream_id)
    result["class_position"] = next(
        (
            row["position"]
            for row in class_summary["ranking"]
            if row["student"].pk == student.pk
        ),
        None,
    )
    result["class_size"] = len(class_summary["ranking"])
    return render(request, "reports/student_report.html", result)


def class_result_view(request, class_id):
    result = class_ranking(class_id)
    class_stream = result["class_stream"]
    subjects = class_stream.classsubject_set.select_related("subject").all()
    return render(
        request,
        "reports/class_report.html",
        {
            "class_stream": class_stream,
            "ranking": result["ranking"],
            "subjects": subjects,
        },
    )


def class_subject_result_view(request, class_id, subject_id):
    result = class_subject_ranking(class_id, subject_id)
    return render(
        request,
        "reports/subject_class_report.html",
        {
            "class_stream": result["class_stream"],
            "subject": result["subject"],
            "ranking": result["ranking"],
        },
    )
