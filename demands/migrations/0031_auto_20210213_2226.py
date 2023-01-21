# Generated by Django 3.1 on 2021-02-13 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0030_auto_20210208_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='contract_type',
            field=models.CharField(blank=True, choices=[('small', '1.5%'), ('medium', '2.0%'), ('big', '50%')], max_length=70, null=True, verbose_name='Contract type'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='ground_floor_excluded',
            field=models.BooleanField(default=False, verbose_name='Ground floor excluded'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='limit_date',
            field=models.DateField(blank=True, null=True, verbose_name='Limit date'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='price_max',
            field=models.IntegerField(blank=True, null=True, verbose_name='Price max'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='price_min',
            field=models.IntegerField(blank=True, null=True, verbose_name='Price min'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='surface_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface max'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='surface_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface min'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='top_floor_excluded',
            field=models.BooleanField(default=False, verbose_name='Top floor excluded'),
        ),
    ]
