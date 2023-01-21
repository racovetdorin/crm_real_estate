# Generated by Django 3.1 on 2020-12-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0060_propertyimage_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentattributes',
            name='built',
            field=models.CharField(choices=[('before_1960', 'Before 1960'), ('between_1960_200', 'Between 1960 - 2000'), ('after_200', 'After 2000')], default='', max_length=256, null=True, verbose_name='Built'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='built',
            field=models.CharField(choices=[('before_1960', 'Before 1960'), ('between_1960_200', 'Between 1960 - 2000'), ('after_200', 'After 2000')], default='', max_length=256, null=True, verbose_name='Built'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='built',
            field=models.CharField(choices=[('before_1960', 'Before 1960'), ('between_1960_200', 'Between 1960 - 2000'), ('after_200', 'After 2000')], default='', max_length=256, null=True, verbose_name='Built'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='built',
            field=models.CharField(choices=[('before_1960', 'Before 1960'), ('between_1960_200', 'Between 1960 - 2000'), ('after_200', 'After 2000')], default='', max_length=256, null=True, verbose_name='Built'),
        ),
    ]
