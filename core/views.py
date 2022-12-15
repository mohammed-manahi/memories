from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import ImageCreateForm
from core.models import Image


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


def image_detail(request, slug, pk):
    # Create image detail view
    image = get_object_or_404(Image, slug=slug, pk=pk)
    template = "core/detail.html"
    context = {"section": "images", "image": image}
    return render(request, template, context)
