from django.contrib import admin
from my_brew_posts.models import UserPost, PostComment

# Register your models here.
admin.site.register(UserPost)
admin.site.register(PostComment)
