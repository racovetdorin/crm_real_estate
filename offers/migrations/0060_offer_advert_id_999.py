# Generated by Django 3.1 on 2022-07-01 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0059_offer_external_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='advert_id_999',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Advert id 999'),
        ),
    ]
