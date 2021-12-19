from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from my_brew_app.models import MyBrewUser, TemporaryUrl

# Register your models here.
UserAdmin.fieldsets += (
    'Personal_Details', {
        'fields': (
            'favorite_beer',
            'city',
            'state',
            'profile_pic',
            'favorites'
        )
    },
),

admin.site.register(MyBrewUser, UserAdmin)
admin.site.register(TemporaryUrl)
