# Generated by Django 3.1 on 2020-11-23 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_auto_20201117_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='prefix_1',
            field=models.CharField(blank=True, choices=[('+40', 'RO +40')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='prefix_2',
            field=models.CharField(blank=True, choices=[('+40', 'RO +40')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='prefix_3',
            field=models.CharField(blank=True, choices=[('+40', 'RO +40')], max_length=20, null=True),
        ),
    ]
