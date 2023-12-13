from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required

from membership.decorators import user_login_check

from .models import CustomUser
from .forms import SignUpForm, EditProfileForm
from .utils import send_token_mail, generate_unique_four_digit_number


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email").lower()
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if (
                CustomUser.objects.filter(email=email).exists()
                or CustomUser.objects.filter(phone=phone).exists()
            ):
                messages.error(request, "User with this email or phone already exists")
                return redirect("signup")

            if password != confirm_password:
                messages.error(request, "Password didn't match!")
                return redirect("signup")

            if len(password) < 5:
                messages.error(request, "Password is short")
                return redirect("signup")

            new_user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=make_password(password),
                role="U",
                token = str(generate_unique_four_digit_number()),
            )
            send_token_mail(email=new_user.email, token=new_user.token)
            messages.success(request, "Pin has been sent to your email. Login and enter pin to verify.")
            return redirect("login")
        else:
            messages.error(request, "Please fill the form with correct details")
    else:
        form = SignUpForm()
    return render(request, "auth/signup.html")


@user_login_check
def login_page(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_or_phone")
        password = request.POST.get("password")

        user = authenticate(request, email_or_phone=email_or_phone, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(
                request, "Email Address/Phone Number or Password didn't match!"
            )
            return redirect("login")
    return render(request, "auth/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if CustomUser.objects.exclude(id=user.id).filter(email=email).exists():
            messages.info(request, f'User with this email "{email}" already exists')
            return redirect("edit_profile")

        if CustomUser.objects.exclude(id=user.id).filter(phone=phone).first():
            messages.info(
                request, f'User with this phone number "{phone}" already exists'
            )
            return redirect("edit_profile")

        if form.is_valid():
            form.save()
            messages.success(request, "Details Updated Successfully")
            return redirect("dashboard")
        else:
            print(form.errors)
            messages.error(request, "Please fill the form with correct data")
    else:
        form = EditProfileForm(instance=user)

    context = {"user": user}
    return render(request, "auth/edit-profile.html", context)


@login_required
def change_password(request):
    user = request.user

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        retype_new_password = request.POST.get("retype_new_password")

        if current_password == "" or new_password == "" or retype_new_password == "":
            messages.error(request, "Please fill all the fields")
            return redirect("change_password")

        if not user.check_password(current_password):
            messages.error(request, "Incorrect Current Password")
            return redirect("change_password")

        if new_password != retype_new_password:
            messages.error(request, "New Passwords didn't match")
            return redirect("change_password")

        if current_password == new_password:
            messages.error(
                request, "New Password should not be same as Current Password!"
            )
            return redirect("change_password")

        user.set_password(new_password)
        user.save()
        messages.success(
            request, "Password Changed Successfully! Login with new password"
        )
        return redirect("login")
    return render(request, "auth/change-password.html")


class CustomPasswordResetView(PasswordResetView):
    """
    Customizing the django default passwordresetview to check if users email exist in
    database before sending mail
    """

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        # Check if the email exists in the database
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "Email does not exist.")
            return self.form_invalid(form)
        return super().form_valid(form)


def verify_user(request):
    user = request.user
    if request.method == "POST":
        pin = request.POST.get("pin")
        if user.token == pin:
            user.is_verified = True
            user.save()
            messages.success(request, "You have been verified")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Pin")
            return redirect("dashboard")
