import random

from django.conf import settings
from django.core.mail import send_mail


def send_token_mail(email, token):
    subject = "Verify Your Account"
    message = f"Your pin is {token}. Login with your new account and enter this pin to verify."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    send_mail(subject, message, email_from, recipient_list)


def generate_unique_four_digit_number():
        four_digit_number = random.randint(1000, 9999)
        return four_digit_number
