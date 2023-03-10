# Generated by Django 3.1 on 2020-12-16 14:50

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0057_featuregroup_is_filtered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuregroup',
            name='property_type',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('house', 'House'), ('apartment', 'Apartment'), ('studio', 'Studio'), ('commercial', 'Commercial space'), ('land', 'Land')], max_length=56, null=True, verbose_name='Property Type'),
        ),
    ]
