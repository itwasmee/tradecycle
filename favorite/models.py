from django.db import models
from ad.models import Ad
from django.contrib.auth.models import User
from tradecycle.settings import AUTH_USER_MODEL

# Create your models here.


class Favorite(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
