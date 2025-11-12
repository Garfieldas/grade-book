from academics.models import Schedule, StudentClass
from users.models import User

def get_student_class(user: User):
    student_class = StudentClass.objects.filter(student=user).first()
    return student_class.school_class

def get_student_teachers(school_class):
    pass
    
