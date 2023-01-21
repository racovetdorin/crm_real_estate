# Generated by Django 3.1 on 2020-09-24 12:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0007_auto_20200924_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='property_type',
            field=models.CharField(choices=[('house', 'House'), ('apartment', 'Apartment'), ('studio', 'Studio'), ('commercial', 'Commercial space'), ('land', 'Land')], default=django.utils.timezone.now, max_length=56),
            preserve_default=False,
        ),
    ]
