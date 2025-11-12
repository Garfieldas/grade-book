from academics.models import Schedule, StudentClass
from users.models import User
<<<<<<< HEAD
from commons.models.days import DAYS_OF_WEEKS
=======

DAYS_OF_WEEKS = (
    ("PIR", "Pirmadienis"),
    ("AN", "Antradienis"),
    ("TRE", "Trečiadienis"),
    ("KET", "Ketvirtadienis"),
    ("PEN", "Penktadienis"),
)
>>>>>>> development

def get_student_class(user: User):
    student_class = StudentClass.objects.filter(student=user).first()
    return student_class.school_class

def get_student_lessons(school_class, day):
    student_lessons = (
        Schedule.objects.select_related("subject__teacher")
        .filter(school_class=school_class, day=day)
    )
    return student_lessons
