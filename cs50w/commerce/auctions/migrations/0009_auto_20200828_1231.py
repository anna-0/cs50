# Generated by Django 3.0.7 on 2020-08-28 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200828_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.Listing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.IntegerField(default=0.01),
        ),
    ]
