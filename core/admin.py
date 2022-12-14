from django.contrib import admin
from core.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # Register image model in admin site
    list_display = ["title", "slug", "image", "created_at"]
    list_filter = ["created_at"]
