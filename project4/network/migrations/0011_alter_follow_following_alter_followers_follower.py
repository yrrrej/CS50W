# Generated by Django 4.0.6 on 2022-07-26 19:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_follow_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(null=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followers',
            name='follower',
            field=models.ManyToManyField(null=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
