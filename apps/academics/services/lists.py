from academics.models import StudentClass, Subject, Schedule, SchoolClass
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

def get_teacher_classes(teacher):
    teacher_classes = (
    SchoolClass.objects
    .filter(schedule__subject__teacher=teacher)
    .distinct()
    )
    return teacher_classes

def get_teacher_students(teacher: User):   
     
    taught_classes = get_teacher_classes(teacher)
    
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

def get_subjects_for_student(student, teacher):
    student_class = get_student_class(student)
    
    subjects = Subject.objects.filter(
        teacher=teacher,
        lessons__school_class=student_class
    ).distinct()
    
    return subjects

def get_class_students(class_id):
    return (
        User.objects
        .filter(
            role=RoleChoices.STUDENT,
            student_class__school_class__id=class_id
        )
        .select_related('student_class', 'student_class__school_class')
        .distinct()
    )