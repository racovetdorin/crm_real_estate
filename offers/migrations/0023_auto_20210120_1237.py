# Generated by Django 3.1 on 2021-01-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0022_auto_20210120_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='contract_number',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='Contract number'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='contract_type',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='Contract type'),
        ),
    ]