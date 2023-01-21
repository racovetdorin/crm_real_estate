# Generated by Django 3.1 on 2020-09-22 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20200915_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.street', verbose_name='Stradă'),
        ),
    ]