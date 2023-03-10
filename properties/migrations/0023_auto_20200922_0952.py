# Generated by Django 3.1 on 2020-09-22 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20200922_0952'),
        ('properties', '0022_auto_20200917_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='location',
        ),
        migrations.AddField(
            model_name='property',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.city', verbose_name='Localitate'),
        ),
        migrations.AddField(
            model_name='property',
            name='number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Număr'),
        ),
        migrations.AddField(
            model_name='property',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.region', verbose_name='Județ'),
        ),
        migrations.AddField(
            model_name='property',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.street', verbose_name='Stradă'),
        ),
        migrations.AddField(
            model_name='property',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.zone', verbose_name='Zonă'),
        ),
    ]
