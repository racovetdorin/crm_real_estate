# Generated by Django 3.1 on 2022-02-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20211104_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rex_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Rex User ID'),
        ),
    ]
