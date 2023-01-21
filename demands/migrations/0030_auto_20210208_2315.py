# Generated by Django 3.1 on 2021-02-08 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0029_demand_key_holding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='contract_type',
            field=models.CharField(blank=True, choices=[('small', '1.5%'), ('medium', '2.0%'), ('big', '50%')], max_length=70, null=True, verbose_name='Contract Type'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='property_type',
            field=models.CharField(blank=True, choices=[('house', 'House'), ('apartment', 'Apartment'), ('studio', 'Studio'), ('commercial', 'Commercial space'), ('land', 'Land'), ('hotel', 'Hotel')], max_length=56, verbose_name='Property type'),
        ),
    ]