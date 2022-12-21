from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    # Create image model and associate many-to-one relation with user model for user creates images
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="images_created", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Associate many-to-many relation with user model for users like the images
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="images_liked", blank=True)
    # Add total likes field to denormalizing counts for image likes
    total_likes = models.PositiveIntegerField(default=0)
    class Meta:
        indexes = [models.Index(fields=["-created_at"]), models.Index(fields=["-total_likes"])]
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Override save method to automatically assign the slug name based on the title using slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Create canonical url for detail view
        return reverse("core:detail", args=[self.pk, self.slug])
