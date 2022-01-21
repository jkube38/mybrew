from django.db import models
from my_brew_app.models import MyBrewUser
from my_brew_posts.models import UserPost, PostComment
from django.utils import timezone


# Create your models here.
class UserPostNotification (models.Model):
    author = models.ForeignKey(
        MyBrewUser,
        related_name='post_author',
        on_delete=models.CASCADE
        )
    user_mentioned = models.ForeignKey(
        MyBrewUser,
        on_delete=models.CASCADE,
        related_name='mentioned_post'
        )
    target = models.ForeignKey(
        UserPost,
        related_name='post_target',
        on_delete=models.CASCADE
        )
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class UserCommentNotification (models.Model):
    author = models.ForeignKey(
        MyBrewUser,
        related_name='comment_author',
        on_delete=models.CASCADE
        )
    user_mentioned = models.ForeignKey(
        MyBrewUser,
        on_delete=models.CASCADE,
        related_name='mentioned_comment'
        )
    target = models.ForeignKey(
        PostComment,
        related_name='comment_target',
        on_delete=models.CASCADE
        )
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
