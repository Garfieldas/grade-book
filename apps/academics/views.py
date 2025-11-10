from django.shortcuts import render
from academics.models import Schedule, StudentClass
from django.contrib.auth.decorators import login_required
from academics.services.lessons import (
    get_student_class,
    DAYS_OF_WEEKS,
    get_student_lessons
)

@login_required
def student_schedule(request):
    user = request.user
    student_class = get_student_class(user)
    monday = get_student_lessons(student_class, DAYS_OF_WEEKS[0][0])
    context = {
        "monday": monday
    }
    return render(request, "academics/schedule/student_shedule.html", context)
