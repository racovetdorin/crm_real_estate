# Generated by Django 3.1 on 2022-03-12 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0024_auto_20220225_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='office_image_url',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Office Image URL'),
        ),
    ]
