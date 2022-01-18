# Generated by Django 3.2 on 2021-12-22 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_app', '0025_alter_userposts_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userposts',
            name='liked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
