from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("new-membership-page/", views.new_membership_page, name="new_membership_page"),
    path("payment/", views.payment_page, name="payment"),
    path(
        "institutional-payment/",
        views.institutional_payment_page,
        name="institutional_payment",
    ),
    path("payment-done/", views.payment_done_page, name="payment_done_page"),
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
    path("initiate-khalti/", views.initiate_khalti, name="initiate_khalti"),
    path(
        "payment-verification/", views.payment_verification, name="payment_verification"
    ),
    path("payment-failed/", views.payment_failed_page, name="payment_failed"),
    path("paypal-success-page/", views.paypal_success_page, name="paypal_success_page"),
    
    path("index/", views.index),
    path("generate-pdf/<int:id>/", views.render_pdf_view, name="generate_pdf"),

    path("send-group-mail/", views.group_mail, name="group_mail"),
    path("create-group/", views.create_group, name="create_group"),
    path("view-gl-details/", views.view_gl_details, name="view_gl_details"),
    path("ins-pdf/", views.render_pdf_view_ins),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
