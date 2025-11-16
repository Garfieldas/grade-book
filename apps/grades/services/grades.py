from grades.models import Mark
from django.utils import timezone

def get_student_grades(student):
    grades = Mark.objects.filter(
        student=student
    ).select_related('subject')

    return grades

def get_recent_grades(student):
    today = timezone.now().date()
    grades = Mark.objects.filter(
        student=student,
        mark_date=today
    ).select_related('subject')
    return grades