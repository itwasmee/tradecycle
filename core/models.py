from django.db import models
from django.contrib.auth.models import User
from ad.models import Ad
from tradecycle.settings import AUTH_USER_MODEL

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='user_profile/')
    activity = models.CharField(max_length=30, default=None)
    location = models.CharField(max_length=30, default=None)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}\'s profile'


class Myad(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
