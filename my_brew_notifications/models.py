from django.db import models
from my_brew_app.models import MyBrewUser
from my_brew_posts.models import UserPost


# Create your models here.
class UserPostNotification (models.Model):
    id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey(MyBrewUser, on_delete=models.CASCADE)
    user_mentioned = models.ForeignKey(
        MyBrewUser,
        on_delete=models.CASCADE,
        related_name='mentioned'
        )
    target_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)


# class BreweryPostNotification (models.Model):
