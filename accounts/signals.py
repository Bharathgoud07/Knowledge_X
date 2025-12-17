from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensure each User always has exactly one Profile.
    Safe even if this signal runs multiple times.
    """
    Profile.objects.get_or_create(user=instance)
