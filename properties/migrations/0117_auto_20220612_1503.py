# Generated by Django 3.1 on 2022-06-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0116_apartmentattributes_rental_fund'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='apartmentattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='basementparkingattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='basementparkingattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='cabinattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='cabinattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='complexattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='complexattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='garageattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='garageattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='hotelattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='hotelattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='landattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='landattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='storageroomattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='storageroomattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='ceiling_height',
            field=models.FloatField(blank=True, null=True, verbose_name='Ceiling height'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='surface_kitchen',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface kitchen'),
        ),
    ]
