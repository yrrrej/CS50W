# Generated by Django 4.0.6 on 2022-07-16 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_bids_listing_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bids',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='comments',
        ),
    ]
