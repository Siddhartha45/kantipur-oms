from django import forms


class SignUpForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()