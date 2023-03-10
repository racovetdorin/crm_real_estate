# Generated by Django 3.1 on 2020-10-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0031_auto_20200929_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentattributes',
            name='key_possession',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='key_possession',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='key_possession',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='key_possession',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
