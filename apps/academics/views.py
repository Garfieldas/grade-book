from django.shortcuts import render
from academics.models import Schedule, StudentClass
from users.models import User

def student_schedule(request):
    user = request.user
    student_class = StudentClass.objects.filter(student=user).first()
    school_class = student_class.school_class if student_class else None
    student_lessons = (
        Schedule.objects.select_related("subject__teacher")
        .filter(school_class=school_class) if school_class else Schedule.objects.none()
    )
    context = {
        "student_lessons": student_lessons
    }
    return render(request, "academics/schedule/student_shedule.html", context)
