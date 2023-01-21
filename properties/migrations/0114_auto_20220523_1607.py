# Generated by Django 3.1 on 2022-05-23 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0113_auto_20220424_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='apartmentattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='basementparkingattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='basementparkingattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='cabinattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='cabinattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='complexattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='complexattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='garageattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='garageattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='hotelattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='hotelattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='storageroomattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='storageroomattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='allow_animals',
            field=models.CharField(blank=True, choices=[('animals_are_accepted', 'Animals are accepted'), ('without_animals', 'Without animals')], max_length=256, null=True, verbose_name='Allow Animals'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='allow_childrens',
            field=models.CharField(blank=True, choices=[('children_are_accepted', 'Children are accepted'), ('without_children', 'Without children')], max_length=256, null=True, verbose_name='Allow Childrens'),
        ),
    ]