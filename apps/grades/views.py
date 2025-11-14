from django.shortcuts import render
from users.decorators import check_roles
from commons.models.roles import RoleChoices

@check_roles(RoleChoices.STUDENT)
def student_grades(request):
    return render(request, "grades/student_grades.html")

@check_roles(RoleChoices.STUDENT)
def newest_grades(request):
    return render(request, "grades/newest_grades.html")
