from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email_or_phone=email, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponse("Successfully logged in {}!".format(user))
        else:
            return HttpResponse("incorrect credentials")
    return render(request, "account/login.html")
