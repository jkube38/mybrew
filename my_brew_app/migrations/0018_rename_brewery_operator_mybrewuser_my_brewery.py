# Generated by Django 3.2 on 2021-05-22 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_app', '0017_auto_20210522_0426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mybrewuser',
            old_name='brewery_operator',
            new_name='my_brewery',
        ),
    ]