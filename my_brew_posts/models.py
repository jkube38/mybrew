from django.db import models
from my_brew_app.models import MyBrewUser
from django.utils import timezone


# Create your models here.
class UserPost(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    post = models.TextField()
    created_by = models.ForeignKey(
        MyBrewUser,
        on_delete=models.CASCADE,
        related_name='user_posts'
    )
    likes = models.IntegerField(blank=True, null=True)
    liked_by = models.ManyToManyField(
        MyBrewUser, symmetrical=False, blank=True)
    post_pic = models.FileField(
        blank=True, null=True, upload_to='images'
    )

    def __str__(self):
        return str(self.id)


class PostComment(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    commenter = models.ForeignKey(
        MyBrewUser,
        on_delete=models.CASCADE,
        related_name='commenting_username'
    )
    post_creator = models.ForeignKey(
        MyBrewUser,
        on_delete=models.CASCADE,
        related_name='post_creator_username'
    )
    target_post = models.ForeignKey(
        UserPost,
        on_delete=models.CASCADE,
        related_name='attach_to'
    )
    comment = models.TextField()
    comment_pic = models.FileField(
        blank=True, null=True, upload_to='images'
    )
    created_at = models.DateTimeField(default=timezone.now)
    embedded_comment = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
