# Generated by Django 3.1 on 2020-09-22 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_location_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='city',
        ),
        migrations.RemoveField(
            model_name='location',
            name='region',
        ),
        migrations.RemoveField(
            model_name='location',
            name='street',
        ),
        migrations.RemoveField(
            model_name='location',
            name='zone',
        ),
    ]