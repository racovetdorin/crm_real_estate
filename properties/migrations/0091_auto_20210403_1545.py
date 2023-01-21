# Generated by Django 3.1 on 2021-04-03 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0090_auto_20210323_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentattributes',
            name='energy_class',
            field=models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], max_length=20, null=True, verbose_name='Energy class'),
        ),
        migrations.AlterField(
            model_name='apartmentattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('block_apartment', 'Block apartment'), ('villa_apartment', 'Villa apartment')], default='block_apartment', max_length=50, null=True, verbose_name='Apartment subtype'),
        ),
        migrations.AlterField(
            model_name='cabinattributes',
            name='energy_class',
            field=models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], max_length=20, null=True, verbose_name='Energy class'),
        ),
        migrations.AlterField(
            model_name='cabinattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('cabin', 'Cabin')], default='cabin', max_length=50, null=True, verbose_name='Cabin subtype'),
        ),
        migrations.AlterField(
            model_name='commercialattributes',
            name='energy_class',
            field=models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], max_length=20, null=True, verbose_name='Energy class'),
        ),
        migrations.AlterField(
            model_name='commercialattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('commercial_space', 'Commercial space'), ('office_space', 'Office space'), ('industrial_space', 'Industrial space')], default='commercial_space', max_length=50, null=True, verbose_name='Commercial subtype'),
        ),
        migrations.AlterField(
            model_name='hotelattributes',
            name='energy_class',
            field=models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], max_length=20, null=True, verbose_name='Energy class'),
        ),
        migrations.AlterField(
            model_name='hotelattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('hotel', 'Hotel'), ('guest_house', 'Guest house')], default='hotel', max_length=50, null=True, verbose_name='Hotel subtype'),
        ),
        migrations.AlterField(
            model_name='houseattributes',
            name='energy_class',
            field=models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], max_length=20, null=True, verbose_name='Energy class'),
        ),
        migrations.AlterField(
            model_name='houseattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('detached', 'Detached house'), ('terraced', 'Terraced house'), ('attached', 'Attached house')], default='detached', max_length=50, null=True, verbose_name='House subtype'),
        ),
        migrations.AlterField(
            model_name='landattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('agricultural_land', 'Agricultural land'), ('construction_land', 'Construction land')], default='agricultural_land', max_length=50, null=True, verbose_name='Land subtype'),
        ),
        migrations.AlterField(
            model_name='studioattributes',
            name='energy_class',
            field=models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], max_length=20, null=True, verbose_name='Energy class'),
        ),
        migrations.AlterField(
            model_name='studioattributes',
            name='subtype',
            field=models.CharField(blank=True, choices=[('studio_apartment', 'Studio apartment')], default='studio_apartment', max_length=50, null=True, verbose_name='Studio subtype'),
        ),
    ]
