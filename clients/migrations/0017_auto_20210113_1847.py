# Generated by Django 3.1 on 2021-01-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_auto_20210102_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_1',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Phone 1'),
        ),
    ]