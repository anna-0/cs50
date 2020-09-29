# Generated by Django 3.0.7 on 2020-08-23 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='startingbid',
            field=models.FloatField(default=0.01),
        ),
    ]
