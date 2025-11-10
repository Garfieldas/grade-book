from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_schedule, name='student_schedule')
]
