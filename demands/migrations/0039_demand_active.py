# Generated by Django 3.1 on 2021-03-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0038_auto_20210322_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]