from django import forms

from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment


class InstitutionalMembershipForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        exclude = ["created_by"]


class GeneralAndLifetimeMembershipForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        exclude = ["created_by", "membership_type"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_ss"]
