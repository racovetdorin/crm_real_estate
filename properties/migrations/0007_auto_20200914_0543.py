# Generated by Django 3.1 on 2020-09-14 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_property_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]