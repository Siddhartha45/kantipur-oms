from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("new-membership-page/", views.new_membership_page, name="new_membership_page"),
    # path(
    #     "institutional-membership/",
    #     views.institutional_membership,
    #     name="institutional_membership",
    # ),
    # path("general-membership/", views.general_membership, name="general_membership"),
    # path("lifetime-membership/", views.lifetime_membership, name="lifetime_membership"),
    # path("student-membership/", views.student_membership, name="student_membership"),
    path("payment/", views.payment_page, name="payment"),
    path(
        "institutional-payment/",
        views.institutional_payment_page,
        name="institutional_payment",
    ),
    path("payment-done/", views.payment_done_page, name="payment_done_page"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path(
        "general-and-lifetime-verification-list/",
        views.general_and_lifetime_membership_verification_list,
        name="gl_verification_list",
    ),
    path(
        "institutional-verification-list/",
        views.institutional_membership_verification_list,
        name="ins_verification_list",
    ),
    path(
        "general-lifetime-membership-verification-page/<int:id>/",
        views.general_and_lifetime_membership_verification_page,
        name="gl_verification_page",
    ),
    path(
        "verify-general-or-lifetime-membership/<int:id>/",
        views.verify_general_or_lifetime_membership,
        name="verify_gl_membership",
    ),
    path(
        "institutional-membership-verification-page/<int:id>/",
        views.institutional_membership_verification_page,
        name="ins_verification_page",
    ),
    path(
        "verify-institutional-membership/<int:id>/",
        views.verify_institution_membership,
        name="verify_ins_membership",
    ),
    path(
        "edit-institutional-membership/<int:id>/",
        views.edit_institutional_membership,
        name="edit_ins_membership",
    ),
    path(
        "edit-gl-membership/<int:id>/",
        views.edit_gl_membership,
        name="edit_gl_membership",
    ),
    path(
        "edit-student-membership/<int:id>/",
        views.edit_student_membership,
        name="edit_student_membership",
    ),
    path(
        "reject-institutional-membership/<int:id>/",
        views.reject_instutional_membership,
        name="reject_ins_membership",
    ),
    path(
        "reject-general-and-lifetime-membership/<int:id>/",
        views.reject_gl_membership,
        name="reject_gl_membership",
    ),
    path("remarks/", views.remarks, name="remarks"),
    path("no-remarks/", views.no_remarks, name="no_remarks"),
    path("upgrade-to-lifetime/", views.upgrade_to_lifetime, name="upgrade_to_lifetime"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
