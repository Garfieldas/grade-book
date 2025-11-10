from django.shortcuts import render, redirect
from users.forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {"form": form})

def LogoutView(request):
    logout(request)
    return redirect('login')