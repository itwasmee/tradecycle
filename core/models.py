from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from tradecycle.settings import AUTH_USER_MODEL

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    # We use ImageKit to manipulate uploaded image
    picture = ProcessedImageField(
        upload_to='user_profile/',
        blank=True,
        processors=[ResizeToFill(128, 128)],
        format='JPEG',
        options={'quality': 100},
        default='profile/user.svg'
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
