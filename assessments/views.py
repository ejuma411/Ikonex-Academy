from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings

from accounts.decorators import staff_required
from assessments.forms import AssessmentForm, GradeScaleForm, ScoreForm
from assessments.models import Assessment, GradeScale, Score
from assessments.results import class_ranking, class_subject_ranking, student_result
from classes.models import ClassStream
from students.models import Student


def render_to_pdf(template_src, context_dict={}):
    """Convert HTML template to PDF"""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    def link_callback(uri, rel):
        """Handle static files in PDF"""
        if uri.startswith('http'):
            return uri
        if uri.startswith('/static/'):
            path = os.path.join(settings.BASE_DIR, 'static', uri.replace('/static/', ''))
            if os.path.exists(path):
                return path
        return uri
    
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), 
        result,
        encoding='UTF-8',
        link_callback=link_callback
    )
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@staff_required
def assessment_list(request):
    assessments = Assessment.objects.all().order_by("-year", "term", "name")
    return render(request, "assessments/list.html", {"assessments": assessments})


@staff_required
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


@staff_required
def assessment_create(request):
    form = AssessmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("assessment_list")
    return render(request, "assessments/create.html", {"form": form})


@staff_required
def assessment_update(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    form = AssessmentForm(request.POST or None, instance=assessment)
    if form.is_valid():
        form.save()
        return redirect("assessment_list")
    return render(request, "assessments/update.html", {"form": form, "assessment": assessment})


@staff_required
def assessment_delete(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    if request.method == "POST":
        assessment.delete()
        return redirect("assessment_list")
    return render(request, "assessments/delete.html", {"assessment": assessment})


@staff_required
def score_list(request):
    scores = Score.objects.select_related("student", "subject", "assessment").order_by(
        "-assessment__year",
        "assessment__name",
        "student__last_name",
        "student__first_name",
    )
    return render(request, "assessments/scores/list.html", {"scores": scores})


@staff_required
def score_detail(request, pk):
    score = get_object_or_404(
        Score.objects.select_related("student", "subject", "assessment"),
        pk=pk,
    )
    return render(request, "assessments/scores/detail.html", {"score": score})


@staff_required
def score_create(request):
    form = ScoreForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("score_list")
    return render(request, "assessments/scores/create.html", {"form": form})


@staff_required
def score_update(request, pk):
    score = get_object_or_404(Score, pk=pk)
    form = ScoreForm(request.POST or None, instance=score)
    if form.is_valid():
        form.save()
        return redirect("score_list")
    return render(request, "assessments/scores/update.html", {"form": form, "score": score})


@staff_required
def score_delete(request, pk):
    score = get_object_or_404(Score, pk=pk)
    if request.method == "POST":
        score.delete()
        return redirect("score_list")
    return render(request, "assessments/scores/delete.html", {"score": score})


@staff_required
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


@staff_required
def class_result_view(request, class_id):
    result = class_ranking(class_id)
    class_stream = result["class_stream"]
    ranking = result["ranking"]
    subjects = class_stream.class_subjects.select_related("subject").all()
    
    # Calculate statistics for the template
    if ranking:
        total_average = sum(item.get('average', 0) for item in ranking)
        class_average = round(total_average / len(ranking), 1) if ranking else 0
        highest_score = max(item.get('total', 0) for item in ranking) if ranking else 0
        pass_count = sum(1 for item in ranking if item.get('grade') not in ['E', 'F', 'N/A'])
        total_students = len(ranking)
    else:
        class_average = 0
        highest_score = 0
        pass_count = 0
        total_students = 0
    
    return render(
        request,
        "reports/class_report.html",
        {
            "class_stream": class_stream,
            "ranking": ranking,
            "subjects": subjects,
            "total_students": total_students,
            "class_average": class_average,
            "highest_score": highest_score,
            "pass_count": pass_count,
            "current_date": timezone.now(),
        },
    )


@staff_required
def class_report_pdf(request, class_id):
    """Generate PDF report for a class"""
    result = class_ranking(class_id)
    class_stream = result["class_stream"]
    ranking = result["ranking"]
    subjects = class_stream.class_subjects.select_related("subject").all()
    
    # Calculate statistics for the template
    if ranking:
        total_average = sum(item.get('average', 0) for item in ranking)
        class_average = round(total_average / len(ranking), 1) if ranking else 0
        highest_score = max(item.get('total', 0) for item in ranking) if ranking else 0
        pass_count = sum(1 for item in ranking if item.get('grade') not in ['E', 'F', 'N/A'])
        total_students = len(ranking)
    else:
        class_average = 0
        highest_score = 0
        pass_count = 0
        total_students = 0
    
    context = {
        "class_stream": class_stream,
        "ranking": ranking,
        "subjects": subjects,
        "total_students": total_students,
        "class_average": class_average,
        "highest_score": highest_score,
        "pass_count": pass_count,
        "current_date": timezone.now(),
        "school_name": "IKONEX ACADEMY",
    }
    
    pdf = render_to_pdf('reports/class_report_pdf.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="class_report_{class_stream.name}_{timezone.now().strftime("%Y%m%d")}.pdf"'
        return response
    
    return HttpResponse("Error generating PDF", status=500)


@staff_required
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


@staff_required
def grade_scale_list(request):
    grade_scales = GradeScale.objects.all().order_by("min_mark")
    return render(request, "assessments/grades/list.html", {"grade_scales": grade_scales})


@staff_required
def grade_scale_create(request):
    form = GradeScaleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("grade_scale_list")
    return render(request, "assessments/grades/create.html", {"form": form})


@staff_required
def grade_scale_update(request, pk):
    grade_scale = get_object_or_404(GradeScale, pk=pk)
    form = GradeScaleForm(request.POST or None, instance=grade_scale)
    if form.is_valid():
        form.save()
        return redirect("grade_scale_list")
    return render(
        request,
        "assessments/grades/update.html",
        {"form": form, "grade_scale": grade_scale},
    )


@staff_required
def grade_scale_delete(request, pk):
    grade_scale = get_object_or_404(GradeScale, pk=pk)
    if request.method == "POST":
        grade_scale.delete()
        return redirect("grade_scale_list")
    return render(request, "assessments/grades/delete.html", {"grade_scale": grade_scale})