# Generated by Django 3.0.7 on 2020-09-02 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20200902_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='startbid',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='currentbid',
        ),
    ]
