from django import forms

from .models import GeneralAndLifetimeMembership, InstitutionalMembership


class InstitutionalMembershipForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        fields = "__all__"


class GeneralAndLifetimeMembershipForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        fields = "__all__"
