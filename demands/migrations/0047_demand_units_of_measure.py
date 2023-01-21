# Generated by Django 3.1 on 2022-01-13 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0046_auto_20220111_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='units_of_measure',
            field=models.CharField(blank=True, choices=[('square_meters', 'Square meters'), ('acres', 'Acres'), ('hectares', 'Hectares')], default='square_meters', max_length=50, null=True, verbose_name='Units of measure'),
        ),
    ]
