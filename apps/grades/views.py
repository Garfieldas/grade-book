from django.shortcuts import render
from django.utils import timezone
from grades.models import Mark
from users.decorators import check_roles
from commons.models.roles import RoleChoices
from apps.grades.forms import AddGrade
from academics.models import Semester, Subject
from users.models import User

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
        if form.is_valid():
            student_id = form.cleaned_data["student"]
            date = form.cleaned_data["date"] or timezone.now()
            mark = form.cleaned_data["value"]
            subject_id = form.cleaned_data["subject"]

            semester = Semester.objects.filter(is_active=True).first()
            student = User.objects.get(pk=student_id)
            subject = Subject.objects.get(pk=subject_id)
            grade = Mark.objects.create(
                student=student,
                subject=subject,
                semester=semester,
                mark_date=date,
                value=mark)
            grade.save()
            print('Works')
        else:
            print(form.errors)
    else:
        form = AddGrade(teacher=teacher)
        print(form.errors)
    return render(request, "grades/add_student_grade_form.html", {"form": form})