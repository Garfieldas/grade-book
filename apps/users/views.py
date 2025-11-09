from django.shortcuts import render
from users.forms import UserLoginForm

def login(request):
    form = UserLoginForm()
    context = {
        "form": form
    }
    return render(request, 'users/login.html', context)