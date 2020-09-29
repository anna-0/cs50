# Generated by Django 3.0.7 on 2020-09-01 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20200901_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='currentbid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price', to='auctions.Bid'),
        ),
    ]