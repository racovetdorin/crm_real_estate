# Generated by Django 3.1 on 2021-01-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0069_auto_20210105_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyimage',
            name='image_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Image name'),
        ),
    ]
