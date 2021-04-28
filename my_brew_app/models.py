from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Breweries(models.Model):
    id = models.IntegerField(auto_created=False, primary_key=True)
    name = models.CharField(max_length=180, null=True)
    brewer_type = models.CharField(max_length=180, null=True)
    street = models.CharField(max_length=180, null=True)
    city = models.CharField(max_length=180, null=True)
    state = models.CharField(max_length=180, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=180, null=True)
    longitude = models.CharField(max_length=180, null=True, blank=True)
    latitude = models.CharField(max_length=180, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True)
    website_url = models.URLField(max_length=350, null=True, blank=True)
    rating_total = models.IntegerField(default=0)
    num_votes = models.IntegerField(default=0)
    rating = models.FloatField(max_length=12, default=0)

    def __str__(self):
        return self.name


class MyBrewUser(AbstractUser):
    favorite_beer = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    profile_pic = models.FileField(
        blank=True, null=True, upload_to='images/'
    )
    favorites = models.ManyToManyField(
        Breweries,
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.username
