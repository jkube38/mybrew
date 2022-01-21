from django.contrib import admin
from my_brew_notifications.models import UserPostNotification
from my_brew_notifications.models import UserCommentNotification


# Register your models here.
admin.site.register(UserPostNotification)
admin.site.register(UserCommentNotification)
