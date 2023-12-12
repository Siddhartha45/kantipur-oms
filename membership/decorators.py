from django.shortcuts import redirect

from .models import GeneralAndLifetimeMembership, InstitutionalMembership


def only_users_without_any_membership(view_func):
    """Only allows users who don't have any type of membership."""

    def wrap(request, *args, **kwargs):
        user = request.user
        general_and_lifetime_membership_does_not_exist = not (
            GeneralAndLifetimeMembership.objects.filter(created_by=user.id).exists()
        )
        institutional_membership_does_not_exist = not (
            InstitutionalMembership.objects.filter(created_by=user.id).exists()
        )
        if (
            user.is_authenticated
            and not user.role == "A"
            and general_and_lifetime_membership_does_not_exist
            and institutional_membership_does_not_exist
        ):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap


def admin_only(view_func):
    """Only allows users with role set to admin."""

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role == "A":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap


def user_login_check(view_func):
    """Restricts authenticated user from visiting the login page."""

    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap


def verified_user(view_func):
    """Restricts unverified users."""

    def wrap(request, *args, **kwargs):
        if request.user.is_verified == True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap
