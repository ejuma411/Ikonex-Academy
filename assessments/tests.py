from decimal import Decimal

from django.test import TestCase

from assessments.forms import ScoreForm
from assessments.models import Assessment, GradeScale, Score
from assessments.results import calculate_grade, class_ranking, student_result
from classes.models import ClassStream
from students.models import Student
from subjects.models import ClassSubject, Subject


class AssessmentResultsTests(TestCase):
    def setUp(self):
        self.class_stream = ClassStream.objects.create(name="Form 1A")
        self.subject_math = Subject.objects.create(code="MATH", name="Mathematics")
        self.subject_english = Subject.objects.create(code="ENG", name="English")
        ClassSubject.objects.create(class_stream=self.class_stream, subject=self.subject_math)
        ClassSubject.objects.create(class_stream=self.class_stream, subject=self.subject_english)

        self.assessment = Assessment.objects.create(
            name="Mid Term",
            total_marks=100,
            term="1",
            year=2026,
        )

        GradeScale.objects.create(grade="A", min_mark=80, max_mark=100)
        GradeScale.objects.create(grade="B", min_mark=60, max_mark=79)
        GradeScale.objects.create(grade="C", min_mark=0, max_mark=59)

        self.student_1 = Student.objects.create(
            admission_no="A001",
            first_name="Ava",
            last_name="Njeri",
            class_stream=self.class_stream,
        )
        self.student_2 = Student.objects.create(
            admission_no="A002",
            first_name="Ben",
            last_name="Otieno",
            class_stream=self.class_stream,
        )

        Score.objects.create(
            student=self.student_1,
            subject=self.subject_math,
            assessment=self.assessment,
            marks=Decimal("85"),
        )
        Score.objects.create(
            student=self.student_1,
            subject=self.subject_english,
            assessment=self.assessment,
            marks=Decimal("75"),
        )
        Score.objects.create(
            student=self.student_2,
            subject=self.subject_math,
            assessment=self.assessment,
            marks=Decimal("70"),
        )
        Score.objects.create(
            student=self.student_2,
            subject=self.subject_english,
            assessment=self.assessment,
            marks=Decimal("68"),
        )

    def test_calculate_grade_uses_configured_scale(self):
        self.assertEqual(calculate_grade(Decimal("86")), "A")
        self.assertEqual(calculate_grade(Decimal("72")), "B+")
        self.assertEqual(calculate_grade(Decimal("30")), "D-")

    def test_score_form_rejects_duplicate_and_out_of_range_scores(self):
        form = ScoreForm(
            data={
                "student": self.student_1.id,
                "subject": self.subject_math.id,
                "assessment": self.assessment.id,
                "marks": "95",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Score already exists for this student, subject, and assessment.",
            str(form.errors),
        )

        form = ScoreForm(
            data={
                "student": self.student_1.id,
                "subject": self.subject_math.id,
                "assessment": self.assessment.id,
                "marks": "120",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Marks cannot exceed the assessment total", str(form.errors))

    def test_student_and_class_results_are_ranked(self):
        student_result_data = student_result(self.student_1)
        self.assertEqual(student_result_data["total"], 160.0)
        self.assertEqual(student_result_data["grade"], "A")
        self.assertEqual(len(student_result_data["subject_summary"]), 2)

        ranking = class_ranking(self.class_stream.id)["ranking"]
        self.assertEqual(ranking[0]["student"], self.student_1)
        self.assertEqual(ranking[0]["position"], 1)
        self.assertEqual(ranking[1]["student"], self.student_2)
        self.assertEqual(ranking[1]["position"], 2)
