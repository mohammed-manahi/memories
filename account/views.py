from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile, Contact


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
            # Create user profile when a new user is created
            Profile.objects.create(user=new_user)
            messages.success(request, "You have been registered successfully")
            template = "account/register_done.html"
            context = {"new_user": new_user}
            return render(request, template, context)
    else:
        user_form = UserRegistrationForm()
        template = "account/register.html"
        context = {"user_form": user_form}
        return render(request, template, context)


@login_required
def edit(request):
    # Create uer edit view to edit user fields in user edit form and profile edit form
    if request.method == "POST":
        # Get the instance since this view performs edit
        user_form = UserEditForm(data=request.POST, instance=request.user)
        # Define files attribute because the profile fields contain photo upload
        profile_form = ProfileEditForm(data=request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully")
        else:
            messages.error(request, "An Error occurred while updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    template = "account/edit.html"
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, template, context)


@login_required
def user_list(request):
    # Create user list view
    users = User.objects.filter(is_active=True, is_staff=False)
    template = "account/list.html"
    context = {"users": users}
    return render(request, template, context)


@login_required
def user_detail(request, username):
    # Create user detail view
    user = get_object_or_404(User, is_active=True, is_staff=False, username=username)
    template = "account/detail.html"
    context = {"section": "people", "user": user}
    return render(request, template, context)


@login_required
@require_POST
def user_follow(request):
    # Create user follow view
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

