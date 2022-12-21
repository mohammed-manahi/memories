from django.contrib import admin
from activity.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    # Register action model in admin site
    list_display = ["user", "verb", "target", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["verb"]
