# Generated by Django 3.1 on 2021-02-13 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0031_auto_20210129_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Offer price'),
        ),
    ]