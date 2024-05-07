from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def sign_in(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('index')
            else:
                messages.error(request, "Identifiant ou mot de passe incorrects.")
                return render(request, 'account/login.html')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrects.")
            return render(request, 'account/login.html')
    return render(request, 'account/login.html', {})


def log_out(request):
    logout(request)
    return redirect('index')

