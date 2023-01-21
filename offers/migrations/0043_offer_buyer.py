# Generated by Django 3.1 on 2021-06-09 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0025_auto_20210609_1424'),
        ('offers', '0042_auto_20210607_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.client', verbose_name='Buyer'),
        ),
    ]