from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST
from core.forms import ImageCreateForm
from core.models import Image
from activity.utils import create_action
import redis
from django.conf import settings

# Setup redis connection to get images view count using redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
            # Record this activity stream using generic relationship of content type
            create_action(request.user, "bookmarked image", new_image)
            messages.success(request, "Image fetched successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
        template = "core/create.html"
        context = {"section": "images", "form": form}
        return render(request, template, context)


@login_required
def image_detail(request, slug, pk):
    # Create image detail view
    image = get_object_or_404(Image, slug=slug, pk=pk)
    # Increment the count of image detail view for each view
    total_views = r.incr(f'image:{image.id}:views')
    template = "core/detail.html"
    context = {"section": "images", "image": image, "total_views": total_views}
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
                # Record this activity stream using generic relationship of content type
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request):
    # Create image list and paginate results
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # Stop ajax fetch api when list reaches the end
            return HttpResponse("")
        images = paginator.page(page.num_pages)
    if images_only:
        template = "core/list_images.html"
        context = {"section": "images", "images": images}
        return render(request, template, context)
    template = "core/list.html"
    context = {"section": "images", "images": images}
    return render(request, template, context)
