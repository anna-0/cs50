# Generated by Django 3.0.7 on 2020-09-02 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_listing_currentbid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='id',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='currentbid',
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='startbid',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Current bid'),
        ),
    ]