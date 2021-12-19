from django.db import models
from django.contrib.auth.models import AbstractUser
from my_brew_brewery.models import MyBrewBrewery


# Create your models here.
class MyBrewUser(AbstractUser):
    favorite_beer = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    favorites = models.ManyToManyField(
        MyBrewBrewery,
        symmetrical=False,
        blank=True
    )
    brewery_owner = models.BooleanField
    profile_pic = models.FileField(
        blank=True, null=True, upload_to='images'
    )

    def __str__(self):
        return self.username


class TemporaryUrl(models.Model):
    snippet = models.CharField(max_length=16)
    user = models.CharField(max_length=150)

    def __str__(self):
        return self.user
