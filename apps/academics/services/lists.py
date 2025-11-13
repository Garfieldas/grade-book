from academics.models import StudentClass, Subject, Schedule, SchoolClass
from users.models import User
from commons.models.roles import RoleChoices

def get_student_class(user: User):
    student_class = StudentClass.objects.filter(student=user)
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

def get_teacher_students(teacher: User):   
     
    taught_classes = (
        Schedule.objects
        .filter(subject__teacher=teacher)
        .values_list('school_class', flat=True)
        .distinct()
    )
    
    students = (
        User.objects
        .filter(
            role=RoleChoices.STUDENT,
            student_class__school_class__id__in=taught_classes 
        )
        .prefetch_related('student_class')
        .distinct()
    )
    
    return students