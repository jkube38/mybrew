# Generated by Django 3.2 on 2021-12-22 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_app', '0028_alter_userposts_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userposts',
            old_name='update',
            new_name='post',
        ),
    ]