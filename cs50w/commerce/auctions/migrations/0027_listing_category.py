# Generated by Django 3.0.7 on 2020-09-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_comment_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[], max_length=10, null=True),
        ),
    ]
