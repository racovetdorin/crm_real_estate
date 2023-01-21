# Generated by Django 3.1 on 2021-03-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0092_merge_20210403_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='latitude',
            field=models.FloatField(blank=True, default=46.769349043202965, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='property',
            name='longitude',
            field=models.FloatField(blank=True, default=23.58974706867647, null=True, verbose_name='Longitude'),
        ),
    ]