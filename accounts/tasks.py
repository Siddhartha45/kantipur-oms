from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import HttpResponse

from celery import shared_task


# @shared_task(bind=True)
def send_token_mail(email, token):
    subject = "Verify Your Account"
    message = f"Your pin is {token}. Login with your new account and enter this pin to verify."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    send_mail(subject, message, email_from, recipient_list)
    return True


# @shared_task(bind=True)
def send_user_mail(self, mail_list):
    subject = "Hello"
    message = f"Your pin i. Login with your new account and enter this pin to verify."
    email_from = settings.EMAIL_HOST_USER
    # mails = GeneralAndLifetimeMembership.objects.filter(membership_type="L").values_list('created_by__email', flat=True)
    # mail_list = [mail for mail in mails]
    recipient_list = mail_list
    send_mail(subject, message, email_from, recipient_list)
    return True

# def aa(request):
#     mails = GeneralAndLifetimeMembership.objects.filter(membership_type="L").values_list('created_by__email', flat=True)
#     mail_list = [mail for mail in mails]
#     send_user_mail.delay(mail_list)
#     return HttpResponse("done")