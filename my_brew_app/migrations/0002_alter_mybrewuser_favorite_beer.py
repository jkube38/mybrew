# Generated by Django 3.2 on 2021-04-23 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybrewuser',
            name='favorite_beer',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
