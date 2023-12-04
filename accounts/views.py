from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from .models import CustomUser
from .forms import SignUpForm


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if password != confirm_password:
                return redirect('signup')

            CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=make_password(password),
                role="U"
            )
            return redirect("login")
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