# Generated by Django 3.1 on 2022-03-16 09:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_auto_20220225_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='external_id',
            field=models.CharField(default=uuid.uuid4, max_length=50, verbose_name='Agent external ID'),
        ),
    ]
