# Generated by Django 3.0.7 on 2020-08-25 14:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200825_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.IntegerField(default=0.01, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]