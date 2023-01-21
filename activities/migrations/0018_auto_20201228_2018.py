# Generated by Django 3.1 on 2020-12-28 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_auto_20201216_1626'),
        ('properties', '0062_auto_20201219_1405'),
        ('demands', '0021_auto_20201208_1628'),
        ('activities', '0017_auto_20201228_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='object_id',
        ),
        migrations.AddField(
            model_name='activity',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.client'),
        ),
        migrations.AddField(
            model_name='activity',
            name='demand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='demands.demand'),
        ),
        migrations.AddField(
            model_name='activity',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='properties.property'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='lead_status',
            field=models.CharField(choices=[('sale', 'Sale Offers'), ('rent', 'Rent Offers'), ('processed', 'Processed')], default='', max_length=256, null=True, verbose_name='Status'),
        ),
    ]