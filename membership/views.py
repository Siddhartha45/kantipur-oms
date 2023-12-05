from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from .forms import (
    InstitutionalMembershipForm,
    GeneralAndLifetimeMembershipForm,
    PaymentForm,
)
from .models import InstitutionalMembership, GeneralAndLifetimeMembership, Payment
from .decorators import only_users_without_any_membership
from . import choices


def dashboard(request):
    return render(request, "mainapp/dashboard.html")


# @only_users_without_any_membership
def new_membership_page(request):
    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES

    context = {"gender": gender, "countries": countries}
    return render(request, "mainapp/new-member.html", context)


def institutional_membership(request):
    if request.method == "POST":
        form = InstitutionalMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            InstitutionalMembership.objects.create(
                created_by=request.user, **form.cleaned_data
            )
            messages.success(
                request,
                "Your membership is under review. We will inform you when verified and after that you can do the payment",
            )
            return redirect("payment")
        else:
            messages.error(request, "Please fill all the fields correctly")
            return redirect("new_membership_page")


def general_membership(request):
    if request.method == "POST":
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            GeneralAndLifetimeMembership.objects.create(
                created_by=request.user, membership_type="G", **form.cleaned_data
            )
            messages.success(
                request,
                "Your membership is under review. We will inform you when verified and after that you can do the payment",
            )
            return redirect("payment")
        else:
            messages.error(request, "Please fill all the fields correctly")
            return redirect("new_membership_page")


def lifetime_membership(request):
    if request.method == "POST":
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(
                created_by=request.user, membership_type="L", **form.cleaned_data
            )
            messages.success(
                request,
                "Your membership is under review. We will inform you when verified and after that you can do the payment",
            )
            return redirect("payment")
        else:
            messages.error(request, "Please fill all the fields correctly")
            return redirect("new_membership_page")


def payment_page(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(user=request.user, **form.cleaned_data)
            return redirect("payment_done_page")
        else:
            print(form.errors)
    else:
        form = PaymentForm()

    return render(request, "mainapp/payment.html")


def payment_done_page(request):
    return render(request, "mainapp/membership-status.html")
