# Generated by Django 3.1 on 2021-12-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0095_auto_20210730_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='recommendation',
            field=models.TextField(blank=True, null=True, verbose_name='Recommendation'),
        ),
    ]