from django.shortcuts import render
from academics.services.lessons import (
    get_student_class,
    DAYS_OF_WEEKS,
    get_student_lessons
)
from django.contrib.auth.decorators import login_required

@login_required
def student_schedule(request):
    user = request.user
    student_class = get_student_class(user)
    monday = get_student_lessons(student_class, DAYS_OF_WEEKS[0][0])
    context = {
        "monday": monday
    }
    return render(request, "academics/schedule/student_schedule.html", context)

@login_required
def teacher_schedule(request):
    return render(request, "academics/schedule/teacher_schedule.html")
