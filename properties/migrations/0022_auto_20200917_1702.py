# Generated by Django 3.1 on 2020-09-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0021_auto_20200917_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_minimum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_per_sqm',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]