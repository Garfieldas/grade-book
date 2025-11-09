from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView, name='login'),
    path('/logout', views.LogoutView, name='logout')
]
