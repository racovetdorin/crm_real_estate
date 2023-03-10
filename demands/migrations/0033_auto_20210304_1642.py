# Generated by Django 3.1 on 2021-03-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0032_auto_20210214_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='key_holding',
        ),
        migrations.AlterField(
            model_name='demand',
            name='property_type',
            field=models.CharField(blank=True, choices=[('house', 'House'), ('apartment', 'Apartment'), ('studio', 'Studio'), ('commercial', 'Commercial space'), ('land', 'Land'), ('hotel', 'Hotel'), ('cabin', 'Cabin')], max_length=56, verbose_name='Property type'),
        ),
    ]
