from django.db import models
from django.contrib.auth.models import AbstractUser
from my_brew_brewery.models import MyBrewBrewery


# Create your models here.
class MyBrewUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    favorite_beer = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    followed_brewery = models.ManyToManyField(
        MyBrewBrewery,
        symmetrical=False,
        blank=True
    )
    followed_user = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True
    )
    brewery_owner = models.BooleanField(default=False)
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
