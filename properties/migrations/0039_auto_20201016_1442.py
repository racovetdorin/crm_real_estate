# Generated by Django 3.1 on 2020-10-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0038_auto_20201015_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='contract_number',
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AddField(
            model_name='property',
            name='contract_type',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]