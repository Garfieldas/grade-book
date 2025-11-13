from django.shortcuts import render
from users.decorators import check_roles
from commons.models.roles import RoleChoices

@check_roles(RoleChoices.STUDENT, RoleChoices.TEACHER)
def home(request):
    return render(request, "dashboard/index.html")

@check_roles(RoleChoices.STUDENT, RoleChoices.TEACHER)
def dashboard(request):
    return render(request, "dashboard/dashboard.html")
