# Generated by Django 3.1 on 2021-02-16 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0013_auto_20210216_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeimage',
            name='deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Deleted'),
        ),
    ]
