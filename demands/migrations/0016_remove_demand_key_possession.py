# Generated by Django 3.1 on 2020-10-22 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0015_auto_20201021_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='key_possession',
        ),
    ]