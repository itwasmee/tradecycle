from django.db import models
from django.contrib.auth.models import User
from tradecycle.settings import AUTH_USER_MODEL

# Create your models here.


class Ad(models.Model):
    title = models.CharField(max_length=20)
    give = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads/photos')
    city = models.CharField(max_length=50)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title
