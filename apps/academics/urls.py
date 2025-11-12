from django.urls import path
from . import views

urlpatterns = [
    path('student', views.student_schedule, name='student_schedule'),
    path('teacher', views.teacher_schedule, name='teacher_schedule')
]
