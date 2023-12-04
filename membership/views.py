from django.shortcuts import render, redirect, HttpResponse

from .forms import InstitutionalMembershipForm, GeneralAndLifetimeMembershipForm
from .models import InstitutionalMembership, GeneralAndLifetimeMembership


def dashboard(request):
    return render(request, "mainapp/dashboard.html")


def new_membership_page(request):
    return render(request, "mainapp/new-member.html")


# def institutional_membership(request):
#     if request.method == "POST":
#         form_type = request.POST.get('form_type')
        
#         if form_type == 'institutional':
#             form = InstitutionalMembershipForm(request.POST, request.FILES)
#             if form.is_valid():
#                 print(form.cleaned_data)
#                 # InstitutionalMembership.objects.create(**form.cleaned_data)
#                 form.save()
#                 return redirect("dashboard")
#             else:
#                 print(form.errors)
#                 return HttpResponse("invalid data")
    
#     else:
#         form1 = InstitutionalMembershipForm()
    
#     return render(request, 'mainapp/new-member.html', {'form1': form1})


def institutional_membership(request):
    if request.method == 'POST':
        form = InstitutionalMembershipForm(request.POST, request.FILES)
        
        if form.is_valid():
            institution_member = form.save(commit=False)
            institution_member.created_by = request.user
            institution_member.save()
            return redirect("dashboard")
        else:
            return redirect("new_membership_page")


def general_membership(request):
    if request.method == 'POST':
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)
        
        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(created_by=request.user, membership_type="G", **form.cleaned_data)
            return redirect("dashboard")
        else:
            return redirect("new_membership_page")


def lifetime_membership(request):
    if request.method == 'POST':
        form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)
        
        if form.is_valid():
            GeneralAndLifetimeMembership.objects.create(created_by=request.user, membership_type="L", **form.cleaned_data)
            return redirect("dashboard")
        else:
            return redirect("new_membership_page")