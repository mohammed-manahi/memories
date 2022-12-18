from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.forms import ImageCreateForm
from core.models import Image


@login_required
def image_create(request):
    # Create image using the bookmarklet
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


@login_required
@require_POST
def image_like(request):
    # Create image like/dislike actions and set http method to post only
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})
