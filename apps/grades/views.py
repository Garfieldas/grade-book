from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from grades.models import Mark
from users.decorators import check_roles
from commons.models.roles import RoleChoices
from apps.grades.forms import AddGrade, GradeModal
from academics.models import Semester
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
            student = form.cleaned_data["student"]
            subject = form.cleaned_data["subject"]
            date = form.cleaned_data["date"] or timezone.now()
            value = form.cleaned_data["value"]

            semester = Semester.objects.filter(is_active=True).first()

            Mark.objects.create(
                student=student,
                subject=subject,
                semester=semester,
                mark_date=date,
                value=value
            )
            messages.success(request, "Pažymis įrašytas sėkmingai!")
            new_form = AddGrade(teacher=teacher)
            return render(
                request,
                "grades/modals/add_student_grade_form.html",
                {"form": new_form})
        else:
            for keys in form.errors.values():
                for error in keys:
                    messages.error(request, error)
            return render(request, "grades/modals/add_student_grade_form.html", {"form": form})
        
    form = AddGrade(teacher=teacher)
    return render(request, "grades/modals/add_student_grade_form.html", {"form": form})


from django.template.loader import render_to_string
@check_roles(RoleChoices.TEACHER)
def add_student_grade_by_id(request, student_id):
    teacher = request.user

    if request.method == "POST":
        form = GradeModal(request.POST, teacher=teacher, student_id=student_id)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            date = form.cleaned_data["date"] or timezone.now()
            value = form.cleaned_data["value"]

            semester = Semester.objects.filter(is_active=True).first()
            student = User.objects.get(pk=student_id)

            Mark.objects.create(
                student=student,
                subject=subject,
                semester=semester,
                mark_date=date,
                value=value
            )
            messages.success(request, f"Pažymis mokiniui {student.first_name} {student.last_name} įrašytas sėkmingai!")
            notifications_html = render_to_string('grades/notifications/alert.html', request=request)
            return HttpResponse(f'<div id="modal-container"></div>{notifications_html}')
        else:
            for keys in form.errors.values():
                for error in keys:
                    messages.error(request, error)
            return render(
                request, 
                "grades/modals/add_student_grade_modal.html", 
                {"form": form, "student_id": student_id}
            )
        
    form = GradeModal(teacher=teacher, student_id=student_id)
    return render(request, "grades/modals/add_student_grade_modal.html", {"form": form, "student_id": student_id})