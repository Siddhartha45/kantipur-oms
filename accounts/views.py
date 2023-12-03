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
    return render()


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email_or_phone=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("Successfully logged in {}!".format(user))
        else:
            return HttpResponse("incorrect credentials")
    return render(request, "account/login.html")


def logout_user(request):
    logout(request)
    return redirect('login')