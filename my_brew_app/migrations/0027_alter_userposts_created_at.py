# Generated by Django 3.2 on 2021-12-22 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_app', '0026_alter_userposts_liked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userposts',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
