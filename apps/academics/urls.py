from django.urls import path
from . import views

urlpatterns = [
    path('teachers_list', views.teachers_table, name='teachers_list'),
    path('students_list/<uuid:class_id>/', views.students_table, name='students_list'),
    path('get_subejcts_for_student/', views.get_subjects_for_student, name='get_subjects_for_student'),
    path('teacher/classes', views.teacher_classes, name='teacher_classes')
]
