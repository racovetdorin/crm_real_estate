# Generated by Django 3.1 on 2021-03-14 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0088_auto_20210313_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AddField(
            model_name='cabinattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AddField(
            model_name='hotelattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AddField(
            model_name='landattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='surface_garden',
            field=models.FloatField(blank=True, null=True, verbose_name='Surface garden m2'),
        ),
        migrations.AlterField(
            model_name='property',
            name='type',
            field=models.CharField(blank=True, choices=[('house', 'House'), ('apartment', 'Apartment'), ('studio', 'Studio'), ('commercial', 'Commercial space'), ('land', 'Land'), ('hotel', 'Hotel'), ('cabin', 'Cabin')], db_index=True, max_length=56, null=True, verbose_name='Type'),
        ),
    ]