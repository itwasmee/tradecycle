from django.db import models
from tradecycle.settings import AUTH_USER_MODEL

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    picture = models.ImageField(
        upload_to='user_profile/', blank=True, default=False
        )
    activity = models.CharField(
        max_length=30, blank=True, default='Non renseigné'
        )
    location = models.CharField(
        max_length=30, blank=True, default='Non renseigné'
        )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}\'s profile'
