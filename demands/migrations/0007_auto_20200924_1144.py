# Generated by Django 3.1 on 2020-09-24 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_delete_multiplezoneslocation'),
        ('demands', '0006_auto_20200924_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='region',
        ),
        migrations.AddField(
            model_name='demand',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.region', verbose_name='Județ'),
        ),
    ]