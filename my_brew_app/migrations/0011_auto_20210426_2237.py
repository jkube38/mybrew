# Generated by Django 3.2 on 2021-04-26 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_app', '0010_auto_20210426_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breweries',
            name='rating_list',
        ),
        migrations.AddField(
            model_name='breweries',
            name='num_votes',
            field=models.IntegerField(default=0, max_length=8),
        ),
        migrations.AddField(
            model_name='breweries',
            name='rating_total',
            field=models.IntegerField(default=0, max_length=8),
        ),
    ]
