from django.shortcuts import render, redirect
from django.utils import timezone
from grades.models import Mark
from django.contrib import messages
from users.decorators import check_roles
from commons.models.roles import RoleChoices
from apps.grades.forms import AddGrade
from academics.models import Semester

@check_roles(RoleChoices.STUDENT)
def student_grades(request):
    return render(request, "grades/student_grades.html")

@check_roles(RoleChoices.STUDENT)
def newest_grades(request):
    return render(request, "grades/newest_grades.html")

@check_roles(RoleChoices.TEACHER)
def add_student_grade(request):
    teacher = request.user
    if request.method == "POST":
        form = AddGrade(request.POST, teacher=teacher)
        subject = request.POST.get('subject')
        print(subject)
        if form.is_valid():
            student = form.cleaned_data["student"]
            subject = form.cleaned_data["subject"]
            date = form.cleaned_data["date"] or timezone.now()
            mark = form.cleaned_data["value"]
            semester = form.cleaned_data["semester"]
            semester = Semester.objects.filter(is_active=True).first()
            grade = Mark.objects.create(
                student=student,
                subject=subject,
                semester=semester,
                mark_date=date,
                value=mark)
            grade.save()
            print('nice')
        else:
            print(form.errors)
    else:
        form = AddGrade(teacher=teacher)
    return render(request, "grades/add_student_grade_form.html", {"form": form})