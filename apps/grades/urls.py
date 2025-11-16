from django.urls import path
from . import views

urlpatterns = [
    path('student_grades', views.student_grades, name='student_grades'),
    path('student_newest_grades', views.newest_grades, name='newest_grades'),
    path('student/add_mark', views.add_student_grade, name='add_mark'),
    path('student/add_mark/<int:student_id>/', views.add_student_grade_by_id, name='add_mark_by_id'),
]
