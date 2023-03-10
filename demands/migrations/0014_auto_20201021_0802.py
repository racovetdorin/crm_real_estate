# Generated by Django 3.1 on 2020-10-21 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0013_auto_20201019_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='attic_excluded',
        ),
        migrations.RemoveField(
            model_name='demand',
            name='new_building',
        ),
        migrations.AddField(
            model_name='demand',
            name='mansard_excluded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='demand',
            name='new_construction',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='demand',
            name='ground_floor_excluded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='demand',
            name='top_floor_excluded',
            field=models.BooleanField(default=False),
        ),
    ]
