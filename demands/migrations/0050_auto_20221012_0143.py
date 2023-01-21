# Generated by Django 3.1 on 2022-10-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0049_auto_20221011_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='closing_date',
            field=models.DateField(blank=True, null=True, verbose_name='Closing date'),
        ),
        migrations.AddField(
            model_name='demand',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Close Demand'),
        ),
    ]
