# Generated by Django 3.1 on 2020-12-16 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_userimage_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='position',
            field=models.IntegerField(default=100, max_length=256, verbose_name='Image Position'),
        ),
    ]
