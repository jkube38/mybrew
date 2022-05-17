from django.db import models


# your models here
class MyBrewBrewery(models.Model):
    brewery_name = models.CharField(max_length=180, null=True)
    brewery_logo = models.ImageField(
        blank=True, null=True, upload_to='brewery_images/'
    )
    brewery_hero_image = models.ImageField(
        blank=True, null=True, upload_to='brewery_images/'
    )
    brewery_bio = models.TextField(null=True)
    brewery_address = models.CharField(max_length=180, null=True)
    brewery_city = models.CharField(max_length=180, null=True)
    brewery_state = models.CharField(max_length=180, null=True)
    brewery_zip = models.CharField(max_length=180, null=True)
    brewery_phone = models.CharField(max_length=10, null=True)
    brewery_website = models.URLField(max_length=350, blank=True, null=True)
    brewery_rating_total = models.IntegerField(default=0)
    brewery_num_votes = models.IntegerField(default=0)
    brewery_rating = models.FloatField(max_length=12, default=0)
    brewery_moderator = models.ForeignKey(
        'my_brew_app.MyBrewUser',
        related_name='brewery_moderator',
        on_delete=models.CASCADE, null=True,
        blank=True
    )
    brewery_email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return self.brewery_name
