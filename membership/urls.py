from django.urls import path

from . import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("new-membership-page/", views.new_membership_page, name="new_membership_page"),
    path(
        "institutional-membership/",
        views.institutional_membership,
        name="institutional_membership",
    ),
    path("general-membership/", views.general_membership, name="general_membership"),
    path("lifetime-membership/", views.lifetime_membership, name="lifetime_membership"),
    path("payment/", views.payment_page, name="payment"),
    path("payment-done/", views.payment_done_page, name="payment_done_page"),
    path("verify-payment", views.verify_payment, name="verify_payment"),
    path("general-and-lifetime-verification-list/", views.general_and_lifetime_membership_verification_list, name="gl_verification_list"),
    path("institutional-verification-list/", views.institutional_membership_verification_list, name="ins_verification_list"),
]
