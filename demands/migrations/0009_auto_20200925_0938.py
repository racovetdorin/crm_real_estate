# Generated by Django 3.1 on 2020-09-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0008_demand_property_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='attic_excluded',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='ground_floor_excluded',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='new_building',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='top_floor_excluded',
            field=models.BooleanField(null=True),
        ),
    ]
