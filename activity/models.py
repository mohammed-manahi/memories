from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    # Create action model
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="actions")
    verb = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add content type to build generic relationship for activity stream with models of installed apps
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="target_object",
                                            on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_id")

    class Meta:
        indexes = [models.Index(fields=["-created_at"]), models.Index(fields=["target_content_type", "target_id"])]
        ordering = ["-created_at"]
