# Generated by Django 3.2 on 2022-01-19 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_brew_notifications', '0002_alter_userpostnotification_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpostnotification',
            name='notification_type',
            field=models.CharField(default='post', max_length=60),
            preserve_default=False,
        ),
    ]
