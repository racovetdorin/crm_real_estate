# Generated by Django 3.1 on 2021-03-23 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('properties', '0089_auto_20210314_0947'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='property',
            unique_together={('attributes_type', 'attributes_object_id')},
        ),
    ]
