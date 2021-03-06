# Generated by Django 3.0.7 on 2020-08-28 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200828_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='startbid',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=8),
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
