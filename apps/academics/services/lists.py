from academics.models import StudentClass, Subject, Schedule
from users.models import User
from commons.models.roles import RoleChoices

def get_student_class(user: User):
    student_class = StudentClass.objects.filter(student=user).first()
    return student_class.school_class

def get_student_teachers(school_class):
    teachers = (
        User.objects
        .filter(role=RoleChoices.TEACHER, subjects__lessons__school_class=school_class)
        .prefetch_related('subjects')
        .distinct()
    )
    teachers_list = []
    for teacher in teachers:
        class_subjects = teacher.subjects.filter(lessons__school_class=school_class).distinct()
        teachers_list.append({
        'teacher': teacher,
        'subjects': class_subjects
    })
    return teachers_list
    
