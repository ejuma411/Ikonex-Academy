from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from assessments.results import class_ranking, student_result
from classes.models import ClassStream
from students.models import Student


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


def report_list(request):
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
            "title": "Reports",
            "class_streams": class_streams,
            "students": students,
            "student_report_name": "student_report_pdf",
            "class_report_name": "class_report_pdf",
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


def student_report_pdf(request, pk):
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    student = get_object_or_404(Student.objects.select_related("class_stream"), pk=pk)
    result = student_result(student)
    buffer, response = _build_pdf_response(f"student-report-{student.admission_no}.pdf")
    doc = _document(buffer)
    styles = _styles()

    story = [
        Paragraph("Ikonex Academy", styles["CenteredTitle"]),
        Spacer(1, 8),
        Paragraph("Student Report Card", styles["Heading2"]),
        Spacer(1, 8),
        Paragraph(f"Name: {student.first_name} {student.last_name}", styles["BodyText"]),
        Paragraph(f"Admission No: {student.admission_no}", styles["BodyText"]),
        Paragraph(f"Class: {student.class_stream.name}", styles["BodyText"]),
        Paragraph(f"Overall Total: {result['total']}", styles["BodyText"]),
        Paragraph(f"Overall Average: {result['average']}", styles["BodyText"]),
        Paragraph(f"Overall Grade: {result['grade']}", styles["BodyText"]),
        Paragraph(
            f"Class Position: {result['class_position']} of {result['class_size']}",
            styles["BodyText"],
        ),
        Spacer(1, 12),
    ]

    table_data = [["Subject", "Total", "Average", "Grade"]]
    for row in result["subject_summary"]:
        table_data.append(
            [
                row["subject_name"],
                f"{row['total']:.2f}",
                f"{row['average']:.2f}",
                row["grade"],
            ]
        )

    story.append(
        Table(
            table_data,
            hAlign="LEFT",
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )
    )

    doc.build(story)
    response.write(buffer.getvalue())
    buffer.close()
    return response


def class_report_pdf(request, class_id):
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    result = class_ranking(class_id)
    class_stream = result["class_stream"]
    safe_name = class_stream.name.replace(" ", "-")
    buffer, response = _build_pdf_response(f"class-report-{safe_name}.pdf")
    doc = _document(buffer)
    styles = _styles()

    story = [
        Paragraph("Ikonex Academy", styles["CenteredTitle"]),
        Spacer(1, 8),
        Paragraph(f"Class Performance Report: {class_stream.name}", styles["Heading2"]),
        Spacer(1, 12),
    ]

    table_data = [["Position", "Student", "Total", "Average", "Grade"]]
    for row in result["ranking"]:
        student = row["student"]
        table_data.append(
            [
                str(row["position"]),
                f"{student.first_name} {student.last_name}",
                f"{row['total']:.2f}",
                f"{row['average']:.2f}",
                row["grade"],
            ]
        )

    story.append(
        Table(
            table_data,
            hAlign="LEFT",
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )
    )

    doc.build(story)
    response.write(buffer.getvalue())
    buffer.close()
    return response
