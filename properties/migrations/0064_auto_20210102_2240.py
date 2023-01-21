# Generated by Django 3.1 on 2021-01-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0063_auto_20210102_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentattributes',
            name='ground_floor',
            field=models.BooleanField(default=False, verbose_name='Ground Floor Excluded'),
        ),
        migrations.AddField(
            model_name='apartmentattributes',
            name='mansard',
            field=models.BooleanField(default=False, verbose_name='Mansard excluded'),
        ),
        migrations.AddField(
            model_name='apartmentattributes',
            name='top_floor',
            field=models.BooleanField(default=False, verbose_name='Top Floor Excluded'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='ground_floor',
            field=models.BooleanField(default=False, verbose_name='Ground Floor Excluded'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='mansard',
            field=models.BooleanField(default=False, verbose_name='Mansard excluded'),
        ),
        migrations.AddField(
            model_name='commercialattributes',
            name='top_floor',
            field=models.BooleanField(default=False, verbose_name='Top Floor Excluded'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='ground_floor',
            field=models.BooleanField(default=False, verbose_name='Ground Floor Excluded'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='mansard',
            field=models.BooleanField(default=False, verbose_name='Mansard excluded'),
        ),
        migrations.AddField(
            model_name='houseattributes',
            name='top_floor',
            field=models.BooleanField(default=False, verbose_name='Top Floor Excluded'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='ground_floor',
            field=models.BooleanField(default=False, verbose_name='Ground Floor Excluded'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='mansard',
            field=models.BooleanField(default=False, verbose_name='Mansard excluded'),
        ),
        migrations.AddField(
            model_name='studioattributes',
            name='top_floor',
            field=models.BooleanField(default=False, verbose_name='Top Floor Excluded'),
        ),
    ]
