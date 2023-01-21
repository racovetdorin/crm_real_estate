# Generated by Django 3.1 on 2022-02-17 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0012_auto_20220215_1145'),
        ('offices', '0020_auto_20220217_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='city_gobal_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city', to='locations.city', verbose_name='Rex ID City'),
        ),
    ]