from django.db import models
from ad.models import Ad
from django.contrib.auth.models import User

# Create your models here.


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
