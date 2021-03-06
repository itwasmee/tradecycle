from django.db import models
from tradecycle.settings import AUTH_USER_MODEL

# Create your models here.


class Ad(models.Model):
    CHOICES = [
        ("O", "Offre"),
        ("C", "Cherche")
    ]
    title = models.CharField(max_length=20)
    action = models.CharField(choices=CHOICES, max_length=1, default=CHOICES[0])
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='ads/photos', blank=True)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    @staticmethod
    def is_favorite(ad, user):
        """confirms if an ad is favorite for a said user
        Arguments:
            ad {object} -- ad to be checked
            user {object} -- user to be checked
        Returns:
            Booleaan -- True if the ad is indeed favorite for the user,
            otherwise False
        """
        if Favorite.objects.filter(ad=ad, user=user).exists():
            return "true"
        else:
            return "false"
