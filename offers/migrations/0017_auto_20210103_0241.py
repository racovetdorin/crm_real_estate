# Generated by Django 3.1 on 2021-01-03 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0016_auto_20210102_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='is_processed',
        ),
        migrations.AddField(
            model_name='offer',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Closed'),
        ),
    ]
