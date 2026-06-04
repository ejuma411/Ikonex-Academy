from django.db import migrations


DEFAULT_GRADE_SCALES = [
    ("A", 80, 100),
    ("A-", 75, 79),
    ("B+", 70, 74),
    ("B", 65, 69),
    ("B-", 60, 64),
    ("C+", 55, 59),
    ("C", 50, 54),
    ("C-", 45, 49),
    ("D+", 40, 44),
    ("D", 35, 39),
    ("D-", 30, 34),
    ("E", 0, 29),
]


def seed_grade_scales(apps, schema_editor):
    GradeScale = apps.get_model("assessments", "GradeScale")
    if GradeScale.objects.exists():
        return

    for grade, min_mark, max_mark in DEFAULT_GRADE_SCALES:
        GradeScale.objects.create(
            grade=grade,
            min_mark=min_mark,
            max_mark=max_mark,
        )


def unseed_grade_scales(apps, schema_editor):
    GradeScale = apps.get_model("assessments", "GradeScale")
    GradeScale.objects.filter(grade__in=[item[0] for item in DEFAULT_GRADE_SCALES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("assessments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_grade_scales, unseed_grade_scales),
    ]
