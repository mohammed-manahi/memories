from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    # Create login form to authenticate users
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    # Create user registration form to register new users
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        # Set form model and fields required rather than password and repeat password fields
        model = User
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        # Check if password and repeat password fields match and its pattern starts with clean_fieldname
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("Passwords don't match")
        return data["password2"]
