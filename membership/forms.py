from django import forms

from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment


class InstitutionalMembershipForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        exclude = ["created_by", "remarks"]


class GeneralAndLifetimeMembershipForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        exclude = ["created_by", "membership_type", "remarks"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_ss"]


class VerificationForm(forms.Form):
    membership_no = forms.CharField()


class InstitutionalMembershipEditForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        exclude = ["created_by", "remarks"]


class GeneralAndLifetimeMembershipEditForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        exclude = ["created_by", "membership_type", "remarks"]


class RejectInstitutionalMembershipForm(forms.Form):
    remarks = forms.CharField()