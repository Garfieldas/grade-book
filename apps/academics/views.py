from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academics.services.lists import get_student_class, get_student_teachers

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