# Generated by Django 3.0.7 on 2020-12-08 20:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20201208_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank='True', related_name='_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
