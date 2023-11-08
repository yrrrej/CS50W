# Generated by Django 4.0.6 on 2022-07-18 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_description_alter_listing_img_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='closedlisting',
            name='closed',
        ),
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.closedlisting'),
        ),
    ]
