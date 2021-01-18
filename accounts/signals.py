from core.models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    """creates a Profile instance when an account is created"""
    if created:
        Profile.objects.create(user=instance)
