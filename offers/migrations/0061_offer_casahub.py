# Generated by Django 3.1 on 2022-09-09 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0060_offer_advert_id_999'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='casahub',
            field=models.BooleanField(default=False, verbose_name='Casahub.md'),
        ),
    ]