from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from account.forms import LoginForm


def user_login(request):
    # Create login view to authenticate users
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Authenticate request using user credentials of form cleaned data
            user = authenticate(request=request, username=data["username"], password=data["password"])
            if user is not None:
                if user.is_active:
                    # Login user into the session if the user exists and active
                    login(request, user)
                    return HttpResponse(f"User {user.username} is authenticated successfully")
                else:
                    return HttpResponse("User is not active")
            else:
                return HttpResponse("Invalid login credentials")
    else:
        form = LoginForm()
    template = "account/login.html"
    context = {"form": form}
    return render(request, template, context)
