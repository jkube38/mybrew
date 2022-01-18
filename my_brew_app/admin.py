from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from my_brew_app.models import MyBrewUser, TemporaryUrl

# Register your models here.
UserAdmin.fieldsets += (
    'Personal_Details', {
        'fields': (
            'brewery_owner',
            'favorite_beer',
            'city',
            'state',
            'profile_pic',
            'followed_brewery',
            'followed_user'
        )
    },
),

admin.site.register(MyBrewUser, UserAdmin)
admin.site.register(TemporaryUrl)
