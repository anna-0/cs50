# Generated by Django 3.0.7 on 2020-08-29 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200828_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='startbid',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=8, verbose_name='Starting bid'),
        ),
    ]