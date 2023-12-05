from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("change-password/", views.change_password, name="change_password"),
    path("forget-password/", views.forget_password, name="forget_password"),
]
