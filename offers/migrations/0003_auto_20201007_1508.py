# Generated by Django 3.1 on 2020-10-07 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_auto_20200929_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='type',
            field=models.CharField(choices=[('sale', 'Sale'), ('rent', 'Rent')], default='sale', max_length=56),
        ),
    ]
