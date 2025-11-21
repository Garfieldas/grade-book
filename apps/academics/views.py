from django.shortcuts import render
from academics.services.lists import (
    get_student_class,
    get_student_teachers,
    get_teacher_students,
    get_teacher_classes,
    get_class_students
)
from users.decorators import check_roles
from commons.models.roles import RoleChoices
from academics.models import Subject
from django.http import HttpResponse

@check_roles(RoleChoices.STUDENT)
def teachers_table(request):
    user = request.user
    student_class = get_student_class(user)
    teachers_list = get_student_teachers(student_class)
    context = {
        "teachers_list": teachers_list,
        "student_class": student_class
    }
    return render(request, "academics/tables/teachers_table.html", context)

@check_roles(RoleChoices.TEACHER)
def students_table(request, class_id):
    students_list = get_class_students(class_id)
    context = {
        "students_list": students_list
    }
    return render(request, "academics/tables/students_table.html", context)

def get_subjects_for_student(request):
    student_id = request.GET.get('student_id')
    teacher = request.user
    if not student_id:
        return HttpResponse('<option value="">Pasirinkite dalyką</option>')
    
    student_class = get_student_class(student_id)
    
    subjects = Subject.objects.filter(
        teacher=teacher,
        lessons__school_class=student_class
    ).distinct()
    
    options = '<option value="">Pasirinkite dalyką</option>'
    for subj in subjects:
        options += f'<option value="{subj.id}">{subj.name}</option>'
    
    return HttpResponse(options)

def teacher_classes(request):
    teacher = request.user
    teacher_classes = get_teacher_classes(teacher)
    context = {
        "teacher_classes": teacher_classes
    }
    return render(request, "academics/tables/teachers_classes_table.html", context)