from django import forms


class LoginForm(forms.Form):
    # Create login form to authenticate users
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
