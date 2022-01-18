# Generated by Django 3.2 on 2022-01-11 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_brew_posts', '0003_userpost_post_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('embedded_comment', models.BooleanField(default=False)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
                ('target_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attach_to', to='my_brew_posts.userpost')),
            ],
        ),
    ]