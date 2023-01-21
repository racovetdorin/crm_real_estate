# Generated by Django 3.1 on 2021-01-28 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0025_auto_20210126_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(blank=True, choices=[('incomplete', 'Incomplete'), ('active', 'Active'), ('transacted', 'Transacted'), ('withdrawn', 'Withdrawn')], default='incomplete', max_length=50, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='type',
            field=models.CharField(blank=True, choices=[('sale', 'Sale'), ('rent', 'Rent')], default='sale', max_length=56, null=True, verbose_name='Type'),
        ),
    ]