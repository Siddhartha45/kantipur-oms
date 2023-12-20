import requests
from datetime import datetime
from pprint import pprint

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    InstitutionalMembershipForm,
    GeneralAndLifetimeMembershipForm,
    PaymentForm,
    VerificationForm,
    InstitutionalMembershipEditForm,
    GeneralAndLifetimeMembershipEditForm,
    RejectMembershipForm,
    StudentMembershipForm,
)
from .models import InstitutionalMembership, GeneralAndLifetimeMembership, Payment
from .decorators import only_users_without_any_membership, admin_only, verified_user
from . import choices


@login_required
def dashboard(request):
    user = request.user
    try:
        gl_user_membership = user.general_and_lifetime_user
    except AttributeError:
        gl_user_membership = None

    try:
        ins_user_membership = user.institutional_user
    except AttributeError:
        ins_user_membership = None

    context = {
        "gl_user_membership": gl_user_membership,
        "ins_user_membership": ins_user_membership,
    }
    return render(request, "mainapp/dashboard.html", context)


@verified_user
@only_users_without_any_membership
def new_membership_page(request):
    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    student_level = choices.STUDENT_LEVEL_CHOICES
    context = {"gender": gender, "countries": countries, "student_level": student_level}
    return render(request, "mainapp/new-member.html", context)


def institutional_membership(request):
    if request.method == "POST":
        form = InstitutionalMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            InstitutionalMembership.objects.create(
                created_by=request.user, **form.cleaned_data
            )
            return redirect("institutional_payment")
        else:
            messages.error(
                request, "Form not saved!!!. Please fill all the fields correctly."
            )
            return redirect("new_membership_page")


def general_membership(request):
    if request.method == "POST":
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(
                created_by=request.user, membership_type="G", **form.cleaned_data
            )
            return redirect("general_payment")
        else:
            messages.error(
                request, "Form not saved!!!. Please fill all the fields correctly."
            )
            return redirect("new_membership_page")


def lifetime_membership(request):
    if request.method == "POST":
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(
                created_by=request.user, membership_type="L", **form.cleaned_data
            )
            return redirect("lifetime_payment")
        else:
            messages.error(
                request, "Form not saved!!!. Please fill all the fields correctly."
            )
            return redirect("new_membership_page")


def general_payment_page(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(
                user=request.user, created_at=datetime.now(), **form.cleaned_data
            )
            return redirect("payment_done_page")
        else:
            messages.error(
                request, "Process Failed!!. Submit Screenshot of your payment."
            )
    else:
        form = PaymentForm()
    return render(request, "mainapp/general_payment.html")


def lifetime_payment_page(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(
                user=request.user, created_at=datetime.now(), **form.cleaned_data
            )
            return redirect("payment_done_page")
        else:
            messages.error(
                request, "Process Failed!!. Submit Screenshot of your payment."
            )
    else:
        form = PaymentForm()
    return render(request, "mainapp/lifetime_payment.html")


def institutional_payment_page(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(
                user=request.user, created_at=datetime.now(), **form.cleaned_data
            )
            return redirect("payment_done_page")
        else:
            messages.error(
                request, "Process Failed!!. Submit Screenshot of your payment."
            )
    else:
        form = PaymentForm()
    return render(request, "mainapp/institutional_payment.html")


@csrf_exempt
def verify_payment(request):
    """To verify the payment done by user using KHALTI."""

    data = request.POST
    user_who_paid = data["product_identity"]
    name = data["product_name"]
    token = data["token"]
    amount = data["amount"]

    url = "https://khalti.com/api/v2/payment/verify/"

    payload = {"token": token, "amount": amount}

    headers = {
        "Authorization": "Key test_secret_key_11ddcd10390443539e267be2691a3486"  # test_secret_key_11ddcd10390443539e267be2691a3486
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    if response.status_code == 200:
        Payment.objects.create(
            created_at=datetime.now(),
            user_id=user_who_paid,
            paid_amount_in_paisa=amount,
        )
        return JsonResponse({"status": "success", "redirect_url": "/payment-done/"})
    else:
        error_message = response.json().get("detail", "Payment verification failed")
        return JsonResponse({"status": "error", "message": error_message}, status=400)


def payment_done_page(request):
    return render(request, "mainapp/membership-status.html")


@admin_only
def general_and_lifetime_membership_verification_list(request):
    members_for_verification = GeneralAndLifetimeMembership.objects.all().order_by(
        "-id"
    )
    context = {"members_for_verification": members_for_verification}
    return render(request, "mainapp/gl_membership_list.html", context)


def general_and_lifetime_membership_verification_page(request, id):
    """Detail Page of General and Lifetime Membership to be viewed by admin."""

    general_or_lifetime_object = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    try:
        latest_membership_no = (
            GeneralAndLifetimeMembership.objects.filter(verification=True)
            .latest("created_at")
            .membership_no
        )
    except GeneralAndLifetimeMembership.DoesNotExist:
        latest_membership_no = "There is no membership number."

    context = {
        "gl": general_or_lifetime_object,
        "latest_membership_no": latest_membership_no,
    }
    if general_or_lifetime_object.membership_type == "S":
        return render(request, "mainapp/student_verification_page.html", context)
    else:
        return render(request, "mainapp/gl-verification-page.html", context)


def verify_general_or_lifetime_membership(request, id):
    verify_object = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    if request.method == "POST":
        form = VerificationForm(request.POST)
        if form.is_valid():
            membership_no = form.cleaned_data.get("membership_no")
            membership_since = form.cleaned_data.get("membership_since")

            verify_object.membership_no = membership_no
            verify_object.membership_since = membership_since
            verify_object.verification = True
            verify_object.verified_date = datetime.now()
            verify_object.save()
            messages.success(request, "Membership Verified")
            return redirect("gl_verification_list")
        else:
            messages.error(
                request,
                "Enter membership number and membership year to verify the member",
            )
            return redirect("gl_verification_page", id=verify_object.id)


@admin_only
def institutional_membership_verification_list(request):
    members_for_verification = InstitutionalMembership.objects.all().order_by("-id")
    context = {"members_for_verification": members_for_verification}
    return render(request, "mainapp/ins_membership_list.html", context)


@admin_only
def institutional_membership_verification_page(request, id):
    """Detail Page of Institutional Membership to be viewed by admin."""

    institution_object = get_object_or_404(InstitutionalMembership, id=id)
    context = {"ins": institution_object}
    return render(request, "mainapp/ins-verification-page.html", context)


@admin_only
def verify_institution_membership(request, id):
    verify_object = get_object_or_404(InstitutionalMembership, id=id)
    verify_object.verification = True
    verify_object.verified_date = datetime.now()
    verify_object.save()
    messages.success(request, "Membership Verified")
    return redirect("ins_verification_list")


def edit_institutional_membership(request, id):
    """
    Let users edit or update their institutional membership details if they are rejected
    by admin.
    """
    instance = get_object_or_404(InstitutionalMembership, id=id)
    user = request.user

    if user.id != instance.created_by.id:
        return redirect("dashboard")

    if user.institutional_user.rejected == False:
        return redirect("index")

    if request.method == "POST":
        form = InstitutionalMembershipEditForm(
            request.POST, request.FILES, instance=instance
        )
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.rejected = False
            form_instance.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            messages.error(request, "Please fill the form with correct data")

    context = {"ins": instance}
    return render(request, "mainapp/edit-ins-membership.html", context)


def edit_gl_membership(request, id):
    """
    Let users edit or update their general or lifetime membership details if they are
    rejected by admin.
    """

    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)
    user = request.user

    if user.id != instance.created_by.id:
        return redirect("dashboard")

    if user.general_and_lifetime_user.rejected == False:
        return redirect("no_remarks")

    if request.method == "POST":
        form = GeneralAndLifetimeMembershipEditForm(
            request.POST, request.FILES, instance=instance
        )
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.rejected = False
            form_instance.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            pprint(form.errors)
            messages.error(request, "Please fill the form with correct data")
    else:
        form = GeneralAndLifetimeMembershipEditForm(instance=instance)
    context = {"gl": instance, "gender": gender, "countries": countries}
    return render(request, "mainapp/edit-gl-membership.html", context)


def reject_instutional_membership(request, id):
    instance = get_object_or_404(InstitutionalMembership, id=id)

    if request.method == "POST":
        form = RejectMembershipForm(request.POST)
        if form.is_valid():
            instance.remarks = form.cleaned_data.get("remarks")
            instance.rejected = True
            instance.save()
            return redirect("ins_verification_list")


def reject_gl_membership(request, id):
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    if request.method == "POST":
        form = RejectMembershipForm(request.POST)
        if form.is_valid():
            instance.remarks = form.cleaned_data.get("remarks")
            instance.rejected = True
            instance.save()
            return redirect("gl_verification_list")


def remarks(request):
    user = request.user
    try:
        gl_or_ins = GeneralAndLifetimeMembership.objects.get(created_by_id=user.id)
        if gl_or_ins.be_subject:
            return redirect("edit_gl_membership", id=gl_or_ins.id)
        else:
            return redirect("edit_student_membership", id=gl_or_ins.id)
    except:
        gl_or_ins = InstitutionalMembership.objects.get(created_by_id=user.id)
        return redirect("edit_ins_membership", id=gl_or_ins.id)


def no_remarks(request):
    return render(request, "mainapp/remarks.html")


def upgrade_to_lifetime(request):
    return render(request, "mainapp/upgrade_to_lifetime.html")


def student_membership(request):
    if request.method == "POST":
        form = StudentMembershipForm(request.POST, request.FILES)

        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(
                created_by=request.user, membership_type="S", **form.cleaned_data
            )
            return redirect("student_payment")
        else:
            messages.error(
                request, "Form not saved!!!. Please fill all the fields correctly."
            )
            return redirect("new_membership_page")


def student_payment_page(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(
                user=request.user, created_at=datetime.now(), **form.cleaned_data
            )
            return redirect("payment_done_page")
        else:
            messages.error(
                request, "Process Failed!!. Submit Screenshot of your payment."
            )
    else:
        form = PaymentForm()
    return render(request, "mainapp/student_payment.html")


def edit_student_membership(request, id):
    """
    Let users edit or update their student membership details if they are rejected by
    admin.
    """

    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    student_level = choices.STUDENT_LEVEL_CHOICES
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)
    user = request.user

    if user.id != instance.created_by.id:
        return redirect("dashboard")

    if user.general_and_lifetime_user.rejected == False:
        return redirect("no_remarks")

    if request.method == "POST":
        form = StudentMembershipForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.rejected = False
            form_instance.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            pprint(form.errors)
            messages.error(request, "Please fill the form with correct data")
    else:
        form = StudentMembershipForm(instance=instance)
    context = {
        "gl": instance,
        "gender": gender,
        "countries": countries,
        "student_level": student_level,
    }
    return render(request, "mainapp/edit_student_membership.html", context)
