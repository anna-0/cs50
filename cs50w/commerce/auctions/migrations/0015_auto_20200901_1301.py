# Generated by Django 3.0.7 on 2020-09-01 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20200830_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='user_id',
            new_name='user',
        ),
    ]
