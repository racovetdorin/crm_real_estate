# Generated by Django 3.1 on 2021-01-03 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0004_auto_20201106_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='email',
            field=models.EmailField(blank=True, max_length=256, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='office',
            name='phone_1',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone 1'),
        ),
        migrations.AddField(
            model_name='office',
            name='phone_2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone 2'),
        ),
        migrations.AddField(
            model_name='office',
            name='phone_3',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone 3'),
        ),
    ]
