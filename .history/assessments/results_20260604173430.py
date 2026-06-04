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
   
# CLASS RANKING SYSTEM
def class_ranking(class_id):
    students = Student.objects.filter(class_stream_id=class_id)

    ranking = []

    for student in students:
        scores = Score.objects.filter(student=student)

        total = scores.aggregate(total=Sum('marks'))['total'] or 0
        avg = scores.aggregate(avg=Avg('marks'))['avg'] or 0

        ranking.append({
            "student": student,
            "total": total,
            "average": round(avg, 2)
        })

    # sort by performance
    ranking = sorted(ranking, key=lambda x: x["total"], reverse=True)

    # assign positions
    position = 1
    for r in ranking:
        r["position"] = position
        position += 1

    return ranking
 
# GRAD