from django.urls import path
from . import views

urlpatterns = [
    path('teachers_list', views.teachers_table, name='teachers_list'),
]
