from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from .models import CustomUser
from .forms import SignUpForm


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get("full_name")
            phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if password != confirm_password:
                return redirect(request)

            CustomUser.objects.create(
                full_name=full_name,
                phone=phone,
                email=email,
                password=make_password(password),
            )
            return HttpResponse("user created")
        else:
            form = SignUpForm()
    return render(request, "auth/signup.html")


def login_page(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_or_phone")
        password = request.POST.get("password")

        user = authenticate(request, email_or_phone=email_or_phone, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("incorrect credentials")
    return render(request, "auth/login.html")


def logout_user(request):
    logout(request)
    return redirect('login')