# Generated by Django 3.2 on 2022-01-29 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_brewery', '0003_auto_20220125_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybrewbrewery',
            name='brewery_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
