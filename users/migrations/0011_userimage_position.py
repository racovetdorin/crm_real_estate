# Generated by Django 3.1 on 2020-12-16 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20201216_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimage',
            name='position',
            field=models.CharField(default='', max_length=256, verbose_name='Image Position'),
        ),
    ]