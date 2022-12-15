from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_image = form.save(commit=False)
            # Associate new image with authenticated user
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image fetched successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
        template = "core/create.html"
        context = {"section": "images", "form": form}
        return render(request, template, context)
