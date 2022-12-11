from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from account.forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


# def user_login(request):
#     # Create login view to authenticate users
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             # Authenticate request using user credentials of form cleaned data
#             user = authenticate(request=request, username=data["username"], password=data["password"])
#             if user is not None:
#                 if user.is_active:
#                     # Login user into the session if the user exists and active
#                     login(request, user)
#                     return HttpResponse(f"User {user.username} is authenticated successfully")
#                 else:
#                     return HttpResponse("User is not active")
#             else:
#                 return HttpResponse("Invalid login credentials")
#     else:
#         form = LoginForm()
#     template = "account/login.html"
#     context = {"form": form}
#     return render(request, template, context)

@login_required
def dashboard(request):
    # Create a dashboard for redirecting authenticated users after login
    template = "account/dashboard.html"
    context = {}
    return render(request, template, context)

def register(request):
    # Create registration and use password check defined in user registration form
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # set password method handles password hashing
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            template = "account/register_done.html"
            context = {"new_user": new_user}
            return render(request, template, context)
    else:
        user_form = UserRegistrationForm()
        template = "account/register.html"
        context = {"user_form": user_form}
        return render(request, template, context)


