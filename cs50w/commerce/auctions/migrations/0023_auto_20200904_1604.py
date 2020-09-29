# Generated by Django 3.0.7 on 2020-09-04 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20200903_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='open',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
