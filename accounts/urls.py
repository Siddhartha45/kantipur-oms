from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("signup/", views.sign_up, name="signup"),
]
