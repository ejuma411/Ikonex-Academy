from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from accounts.decorators import staff_required
from assessments.results import class_ranking, student_result
from classes.models import ClassStream
from students.models import Student


@staff_required
def result_list(request):
    class_streams = ClassStream.objects.all().order_by("name")
    students = Student.objects.select_related("class_stream").order_by(
        "class_stream__name",
        "last_name",
        "first_name",
    )
    return render(
        request,
        "reports/index.html",
        {
            "title": "Results",
            "class_streams": class_streams,
            "students": students,
            "student_report_name": "student_result",
            "class_report_name": "class_result",
        },
    )


@staff_required
def report_list(request):
    class_streams = ClassStream.objects.all().order_by("name")
    students = Student.objects.select_related("class_stream").order_by(
        "class_stream__name",
        "last_name",
        "first_name",
    )
    
    # Annotate student count for each class
    from django.db.models import Count
    class_streams = class_streams.annotate(student_count=Count('students'))
    
    return render(
        request,
        "reports/index.html",
        {
            "title": "Reports",
            "class_streams": class_streams,
            "students": students,
            "student_report_name": "student_report_pdf",  # For PDF download
            "class_report_name": "class_report_pdf",      # For PDF download
            "student_preview_name": "student_result_view",  # For HTML preview
            "class_preview_name": "class_result_view",      # For HTML preview
        },
    )


def _build_pdf_response(filename):
    buffer = BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return buffer, response


def _document(buffer):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate

    return SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )


def _styles():
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CenteredTitle",
            parent=styles["Title"],
            alignment=1,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    return styles


from assessments.pdf_generator import StudentReportPDF
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from students.models import Student


@staff_required
def student_report_pdf(request, student_id):
    """Generate professional PDF report for a student"""
    student = get_object_or_404(Student.objects.select_related('class_stream'), pk=student_id)
    
    # Get student results
    result = student_result(student)
    class_summary = class_ranking(student.class_stream_id)
    
    # Get class position
    class_position = next(
        (
            row["position"]
            for row in class_summary["ranking"]
            if row["student"].pk == student.pk
        ),
        None,
    )
    class_size = len(class_summary["ranking"])
    
    # Extract data
    scores = result.get('scores', [])
    subject_summary = result.get('subject_summary', [])
    total = result.get('total', 0)
    average = result.get('average', 0)
    grade = result.get('grade', 'N/A')
    
    # Generate PDF
    buffer = BytesIO()
    pdf_generator = StudentReportPDF(
        buffer, student, scores, subject_summary, 
        total, average, grade, class_position, class_size
    )
    pdf_generator.generate()
    
    buffer.seek(0)
    
    # Return PDF response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="student_report_{student.admission_no}_{timezone.now().strftime("%Y%m%d")}.pdf"'
    return response

from io import BytesIO
from django.http import HttpResponse
from django.utils import timezone
from assessments.pdf_generator import ProfessionalReportPDF


@staff_required
def class_report_pdf(request, class_id):
    """Generate professional PDF report for a class using ReportLab"""
    result = class_ranking(class_id)
    class_stream = result["class_stream"]
    ranking = result["ranking"]
    subjects = class_stream.class_subjects.select_related('subject').all()
    
    # Calculate statistics
    if ranking:
        total_students = len(ranking)
        class_average = sum(item['average'] for item in ranking) / len(ranking)
        highest_score = max(item['total'] for item in ranking)
        pass_count = sum(1 for item in ranking if item['grade'] not in ['E', 'F', 'N/A'])
    else:
        total_students = 0
        class_average = 0
        highest_score = 0
        pass_count = 0
    
    stats = {
        'total_students': total_students,
        'class_average': round(class_average, 1),
        'highest_score': highest_score,
        'pass_count': pass_count,
    }
    
    # Generate PDF
    buffer = BytesIO()
    pdf_generator = ProfessionalReportPDF(buffer, class_stream, ranking, subjects, stats)
    pdf_generator.generate()
    
    buffer.seek(0)
    
    # Return PDF response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="class_report_{class_stream.name}_{timezone.now().strftime("%Y%m%d")}.pdf"'
    return response