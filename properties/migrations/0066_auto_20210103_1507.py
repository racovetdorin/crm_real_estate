# Generated by Django 3.1 on 2021-01-03 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0065_auto_20210103_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentattributes',
            name='balconies_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Balconies number'),
        ),
        migrations.AlterField(
            model_name='apartmentattributes',
            name='bathrooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Bathrooms number'),
        ),
        migrations.AlterField(
            model_name='apartmentattributes',
            name='kitchens_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Kitchens number'),
        ),
        migrations.AlterField(
            model_name='apartmentattributes',
            name='rooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3)], null=True, verbose_name='Rooms number'),
        ),
        migrations.AlterField(
            model_name='commercialattributes',
            name='balconies_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Balconies number'),
        ),
        migrations.AlterField(
            model_name='commercialattributes',
            name='bathrooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Bathrooms number'),
        ),
        migrations.AlterField(
            model_name='commercialattributes',
            name='kitchens_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Kitchens number'),
        ),
        migrations.AlterField(
            model_name='commercialattributes',
            name='rooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3)], null=True, verbose_name='Rooms number'),
        ),
        migrations.AlterField(
            model_name='houseattributes',
            name='balconies_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Balconies number'),
        ),
        migrations.AlterField(
            model_name='houseattributes',
            name='bathrooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Bathrooms number'),
        ),
        migrations.AlterField(
            model_name='houseattributes',
            name='kitchens_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Kitchens number'),
        ),
        migrations.AlterField(
            model_name='houseattributes',
            name='rooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3)], null=True, verbose_name='Rooms number'),
        ),
        migrations.AlterField(
            model_name='studioattributes',
            name='balconies_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Balconies number'),
        ),
        migrations.AlterField(
            model_name='studioattributes',
            name='bathrooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Bathrooms number'),
        ),
        migrations.AlterField(
            model_name='studioattributes',
            name='kitchens_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Kitchens number'),
        ),
        migrations.AlterField(
            model_name='studioattributes',
            name='rooms_number',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3)], null=True, verbose_name='Rooms number'),
        ),
    ]
