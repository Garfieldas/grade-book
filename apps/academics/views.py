from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academics.services.lists import get_student_class, get_student_teachers, get_teacher_students

@login_required
def teachers_table(request):
    user = request.user
    student_class = get_student_class(user)
    teachers_list = get_student_teachers(student_class)
    context = {
        "teachers_list": teachers_list,
        "student_class": student_class
    }
    return render(request, "academics/tables/teachers_table.html", context)

@login_required
def students_table(request):
    user = request.user
    students_list = get_teacher_students(user)
    context = {
        "students_list": students_list
    }
    return render(request, "academics/tables/students_table.html", context)