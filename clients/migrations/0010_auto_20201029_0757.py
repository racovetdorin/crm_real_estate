# Generated by Django 3.1 on 2020-10-29 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20201016_1442'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='owner',
            new_name='user',
        ),
    ]