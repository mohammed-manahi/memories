from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from core.models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    # Create signal to count user likes using m2m which indicates many-to-many relationship
    instance.total_likes = instance.users_like.count()
    instance.save()
