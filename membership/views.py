import requests
import json

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    InstitutionalMembershipForm,
    GeneralAndLifetimeMembershipForm,
    PaymentForm,
    VerificationForm,
    InstitutionalMembershipEditForm,
    GeneralAndLifetimeMembershipEditForm
)
from .models import InstitutionalMembership, GeneralAndLifetimeMembership, Payment
from .decorators import only_users_without_any_membership, admin_only
from . import choices


@login_required
def dashboard(request):
    user = request.user
    try:
        user_membership = user.general_and_lifetime_user
        print(user_membership)
    except ObjectDoesNotExist:
        user_membership = None
    context = {"user_membership": user_membership}
    return render(request, "mainapp/dashboard.html", context)


@only_users_without_any_membership
def new_membership_page(request):
    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    context = {"gender": gender, "countries": countries}
    return render(request, "mainapp/new-member.html", context)


def institutional_membership(request):
    if request.method == "POST":
        form = InstitutionalMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            InstitutionalMembership.objects.create(
                created_by=request.user, **form.cleaned_data
            )
            messages.success(
                request,
                "Your membership is under review. We will inform you when verified and after that you can do the payment",
            )
            return redirect("payment")
        else:
            print(form.errors)
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
            messages.error(request, "Submit Screenshot of your payment.")
            print(form.errors)
    else:
        form = PaymentForm()
    return render(request, "mainapp/payment.html")


@csrf_exempt
def verify_payment(request):
    data = request.POST
    user_who_paid = data['product_identity']
    name = data['product_name']
    token = data['token']
    amount = data['amount']

    url = "https://khalti.com/api/v2/payment/verify/"
    
    payload = {
    "token": token,
    "amount": amount
    }
    
    headers = {
    "Authorization": "Key test_secret_key_11ddcd10390443539e267be2691a3486"             #test_secret_key_11ddcd10390443539e267be2691a3486
    }
    

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    
    if response.status_code == 200:
        Payment.objects.create(user_id=user_who_paid, paid_amount_in_paisa=amount)
    else:
        error_message = response.json().get('detail', 'Payment verification failed')
        return JsonResponse({"status": "error", "message": error_message}, status=400)


def payment_done_page(request):
    return render(request, "mainapp/membership-status.html")


@admin_only
def general_and_lifetime_membership_verification_list(request):
    members_for_verification = GeneralAndLifetimeMembership.objects.all()
    context = {"members_for_verification": members_for_verification}
    return render(request, "mainapp/gl_membership_list.html", context)


def general_and_lifetime_membership_verification_page(request, id):
    general_or_lifetime_object = get_object_or_404(GeneralAndLifetimeMembership, id=id)
    context = {"gl": general_or_lifetime_object}
    return render(request, "mainapp/gl-verification-page.html", context)


def verify_general_or_lifetime_membership(request, id):
    verify_object = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    if request.method == "POST":
        form = VerificationForm(request.POST)
        if form.is_valid():
            membership_no = form.cleaned_data.get("membership_no")
            verify_object.membership_no = membership_no
            verify_object.verification = True
            verify_object.save()
            messages.success(request, "Membership Verified")
            return redirect("gl_verification_list")
        else:
            messages.error(request, "Enter membership number to verify the member")
            return redirect("gl_verification_page", id=verify_object.id)


@admin_only
def institutional_membership_verification_list(request):
    members_for_verification = InstitutionalMembership.objects.all().order_by("-id")
    context = {"members_for_verification": members_for_verification}
    return render(request, "mainapp/ins_membership_list.html", context)


@admin_only
def institutional_membership_verification_page(request, id):
    institution_object = get_object_or_404(InstitutionalMembership, id=id)
    context = {"ins": institution_object}
    return render(request, "mainapp/ins-verification-page.html", context)


@admin_only
def verify_institution_membership(request, id):
    verify_object = get_object_or_404(InstitutionalMembership, id=id)
    verify_object.verification = True
    verify_object.save()
    messages.success(request, "Membership Verified")
    return redirect("ins_verification_list")


def edit_institutional_membership(request, id):
    """Let users edit or update their institutional membership details if they are rejected by admin."""
    instance = get_object_or_404(InstitutionalMembership, id=id)
    
    if request.user.id != instance.created_by.id:
        return redirect("dashboard")
    
    if request.method == "POST":
        form = InstitutionalMembershipEditForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            messages.error(request, "Please fill the form with correct data")
    
    context = {"ins": instance}
    return render(request, "mainapp/edit-ins-membership.html", context)


def edit_gl_membership(request, id):
    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)
    
    if request.method == "POST":
        form =  GeneralAndLifetimeMembershipEditForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
    else:
        form = GeneralAndLifetimeMembershipEditForm(instance=instance)
    context = {"gl": instance, "gender": gender, "countries": countries}
    return render(request, "mainapp/edit-gl-membership.html", context)