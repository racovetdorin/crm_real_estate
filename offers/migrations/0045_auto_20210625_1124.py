# Generated by Django 3.1 on 2021-06-25 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0044_offer_withdrawn_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='commission_percent',
            field=models.FloatField(blank=True, null=True, verbose_name='Commission %'),
        ),
    ]
