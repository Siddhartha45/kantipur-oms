from django.shortcuts import render, redirect, HttpResponse

from .forms import InstitutionalMembershipForm, GeneralAndLifetimeMembershipForm
from .models import InstitutionalMembership, GeneralAndLifetimeMembership
from . import choices


def dashboard(request):
    return render(request, "mainapp/dashboard.html")


def new_membership_page(request):
    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    
    context = {'gender': gender, 'countries': countries}
    return render(request, "mainapp/new-member.html", context)


def institutional_membership(request):
    if request.method == 'POST':
        form = InstitutionalMembershipForm(request.POST, request.FILES)
        
        if form.is_valid():
            InstitutionalMembership.objects.create(created_by=request.user, **form.cleaned_data)
            return redirect("dashboard")
        else:
            return redirect("new_membership_page")


def general_membership(request):
    if request.method == 'POST':
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)
        
        if form.is_valid():
            print(form.cleaned_data)
            GeneralAndLifetimeMembership.objects.create(created_by=request.user, membership_type="G", **form.cleaned_data)
            return redirect("dashboard")
        else:
            print(form.errors)
            return redirect("new_membership_page")


def lifetime_membership(request):
    if request.method == 'POST':
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)
        
        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(created_by=request.user, membership_type="L", **form.cleaned_data)
            return redirect("dashboard")
        else:
            return redirect("new_membership_page")