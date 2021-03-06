# Generated by Django 3.0.7 on 2020-09-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_auto_20200917_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('HOM', 'Home'), ('ELC', 'Electronics'), ('FSN', 'Fashion'), ('PET', 'Pets'), ('LES', 'Leisure'), ('SUP', 'Supplies')], max_length=3),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
