# Generated by Django 3.0.7 on 2020-08-30 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200829_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watching',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing'),
            preserve_default=False,
        ),
    ]