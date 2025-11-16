from grades.models import Mark
from users.models import User
from academics.models import Subject

def get_student_grades(student):
    grades = Mark.objects.filter(
        student=student
    ).prefetch_related('subject')

    return grades