# Generated by Django 3.1 on 2020-12-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_activity_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('sale', 'Sale Offers'), ('rent', 'Rent Offers'), ('allocated', 'Allocated'), ('done', 'Done')], default='sale', max_length=20, null=True, verbose_name='Status'),
        ),
    ]
