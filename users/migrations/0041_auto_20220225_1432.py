# Generated by Django 3.1 on 2022-02-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_auto_20220222_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='external_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Agent external ID'),
        ),
    ]
