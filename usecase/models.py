from django.db import models

# Create your models here.


class Usecase(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='usecase/')
