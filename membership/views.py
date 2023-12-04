from django.shortcuts import render


def dashboard(request):
    return render(request, "mainapp/dashboard.html")


def membership(request):
    return render(request, "mainapp/new-member.html")