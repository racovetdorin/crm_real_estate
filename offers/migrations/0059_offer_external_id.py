# Generated by Django 3.1 on 2022-04-21 15:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0058_auto_20220418_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='external_id',
            field=models.CharField(default=uuid.uuid4, max_length=50, verbose_name='Offer external ID'),
        ),
    ]
