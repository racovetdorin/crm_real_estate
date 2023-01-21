# Generated by Django 3.1 on 2020-11-06 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0011_auto_20201106_1534'),
        ('offices', '0004_auto_20201106_1534'),
        ('demands', '0017_auto_20201104_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to='clients.client', verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='comments',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='contract_number',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Contract Number'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='contract_type',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Contract Type'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Deleted At'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='furnished',
            field=models.BooleanField(default=False, verbose_name='Furnished'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='garage',
            field=models.BooleanField(default=False, verbose_name='Garage'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='ground_floor_excluded',
            field=models.BooleanField(default=False, verbose_name='Ground Floor Excluded'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='limit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Limit Date'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='mansard_excluded',
            field=models.BooleanField(default=False, verbose_name='Mansard Excluded'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='new_construction',
            field=models.BooleanField(default=False, verbose_name='New Construction'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to='offices.office', verbose_name='Office'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='parking_spot',
            field=models.BooleanField(default=False, verbose_name='Parking Spot'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='pet_friendly',
            field=models.BooleanField(default=False, verbose_name='Pet Friendly'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='price_max',
            field=models.IntegerField(blank=True, null=True, verbose_name='Price Max'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='price_min',
            field=models.IntegerField(blank=True, null=True, verbose_name='Price Min'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='property_type',
            field=models.CharField(blank=True, choices=[('house', 'House'), ('apartment', 'Apartment'), ('studio', 'Studio'), ('commercial', 'Commercial space'), ('land', 'Land')], max_length=56, verbose_name='Property Type'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='rooms_max',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], null=True, verbose_name='Rooms Max'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='rooms_min',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], null=True, verbose_name='Rooms Min'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='surface_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface Max'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='surface_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface Min'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='top_floor_excluded',
            field=models.BooleanField(default=False, verbose_name='Top Floor Excluded'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated At'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to=settings.AUTH_USER_MODEL, verbose_name='Agent'),
        ),
    ]
