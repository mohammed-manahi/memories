from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    # Create profile model which extends default user model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Contact(models.Model):
    # Create contact model to build follow system
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rel_from_set")
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rel_to_set")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Set database index to created at field since django automatically sets indexes for foreign keys
        indexes = [models.Index(fields=["-created_at"]), ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# Customize the user model by adding many-to-many relationships dynamically which doesn't imply changes in database
# This customization enables user.followers.all() and user.following.all()
user_model = get_user_model()
# Set symmetrical to false which sets the follow from one side and doesn't enforce mutual following by default
# If user 1 followed user 2 the relationship doesn't enforce user 2 to follow user 1 automatically
user_model.add_to_class = (
    "following", models.ManyToManyField("self", through=Contact, related_name="followers", symmetrical=False))
