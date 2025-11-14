from django.shortcuts import render
from users.decorators import check_roles
from commons.models.roles import RoleChoices
from apps.grades.forms import AddGrade

@check_roles(RoleChoices.STUDENT)
def student_grades(request):
    return render(request, "grades/student_grades.html")

@check_roles(RoleChoices.STUDENT)
def newest_grades(request):
    return render(request, "grades/newest_grades.html")

def add_student_grade(request):
    teacher = request.user

    form = AddGrade(teacher=teacher)

    return render(request, "grades/add_student_grade_form.html", {"form": form})