from django import forms

from .models import CustomUser


class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.IntegerField()
    password = forms.CharField()
    confirm_password = forms.CharField()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]