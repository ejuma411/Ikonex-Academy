from django.db.models import Sum, Avg
from students.models import Student
from assessments.models import Score
from classes.models import ClassStream


# --------------------------
# STUDENT PERFORMANCE ENGINE
# --------------------------

def student_result(student_id):
    scores = Score.objects.filter(student_id=student_id)

    total = scores.aggregate(total=Sum('marks'))['total'] or 0
    average = scores.aggregate(avg=Avg('marks'))['avg'] or 0

    return {
        "total": total,
        "average": round(average, 2),
        "scores": scores
    }
    
   