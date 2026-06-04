from decimal import Decimal

from django.db.models import Avg, Sum

from assessments.models import GradeScale, Score
from classes.models import ClassStream
from students.models import Student
from subjects.models import Subject


def _to_number(value):
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _rounded(value):
    return round(float(_to_number(value)), 2)


def calculate_grade(mark):
    grade = GradeScale.objects.filter(
        min_mark__lte=mark,
        max_mark__gte=mark,
    ).order_by("-min_mark").first()
    return grade.grade if grade else "N/A"


def student_result(student):
    if isinstance(student, int):
        student = Student.objects.select_related("class_stream").get(pk=student)

    scores = (
        Score.objects.filter(student=student)
        .select_related("subject", "assessment")
        .order_by("subject__name", "assessment__year", "assessment__name")
    )
    subject_summary = (
        Score.objects.filter(student=student)
        .values("subject_id", "subject__code", "subject__name")
        .annotate(total=Sum("marks"), average=Avg("marks"))
        .order_by("subject__name")
    )

    total = scores.aggregate(total=Sum("marks"))["total"] or Decimal("0")
    average = scores.aggregate(average=Avg("marks"))["average"] or Decimal("0")
    class_summary = class_ranking(student.class_stream_id)
    class_position = next(
        (
            row["position"]
            for row in class_summary["ranking"]
            if row["student"].pk == student.pk
        ),
        None,
    )

    return {
        "student": student,
        "scores": scores,
        "subject_summary": [
            {
                "subject_id": row["subject_id"],
                "subject_code": row["subject__code"],
                "subject_name": row["subject__name"],
                "total": _rounded(row["total"]),
                "average": _rounded(row["average"]),
                "grade": calculate_grade(row["average"] or 0),
            }
            for row in subject_summary
        ],
        "total": _rounded(total),
        "average": _rounded(average),
        "grade": calculate_grade(average),
        "class_position": class_position,
        "class_size": len(class_summary["ranking"]),
    }


def class_ranking(class_id):
    class_stream = ClassStream.objects.get(pk=class_id)
    students = Student.objects.filter(class_stream=class_stream).select_related("class_stream")

    ranking = []
    for student in students:
        scores = Score.objects.filter(student=student)
        total = scores.aggregate(total=Sum("marks"))["total"] or Decimal("0")
        average = scores.aggregate(average=Avg("marks"))["average"] or Decimal("0")
        ranking.append(
            {
                "student": student,
                "total": _rounded(total),
                "average": _rounded(average),
                "grade": calculate_grade(average),
            }
        )

    ranking.sort(
        key=lambda row: (
            -row["total"],
            -row["average"],
            row["student"].first_name.lower(),
            row["student"].last_name.lower(),
        )
    )

    for position, row in enumerate(ranking, start=1):
        row["position"] = position

    return {
        "class_stream": class_stream,
        "ranking": ranking,
    }


def class_subject_ranking(class_id, subject_id):
    class_stream = ClassStream.objects.get(pk=class_id)
    subject = Subject.objects.get(pk=subject_id)
    students = Student.objects.filter(class_stream=class_stream).select_related("class_stream")

    ranking = []
    for student in students:
        scores = Score.objects.filter(student=student, subject=subject)
        total = scores.aggregate(total=Sum("marks"))["total"] or Decimal("0")
        average = scores.aggregate(average=Avg("marks"))["average"] or Decimal("0")
        ranking.append(
            {
                "student": student,
                "total": _rounded(total),
                "average": _rounded(average),
                "grade": calculate_grade(average),
            }
        )

    ranking.sort(
        key=lambda row: (
            -row["total"],
            -row["average"],
            row["student"].first_name.lower(),
            row["student"].last_name.lower(),
        )
    )

    for position, row in enumerate(ranking, start=1):
        row["position"] = position

    return {
        "class_stream": class_stream,
        "subject": subject,
        "ranking": ranking,
    }
