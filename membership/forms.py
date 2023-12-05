from django import forms

from .models import GeneralAndLifetimeMembership, InstitutionalMembership


class InstitutionalMembershipForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        exclude = ["created_by"]


class GeneralAndLifetimeMembershipForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        exclude = ["created_by", "membership_type"]
