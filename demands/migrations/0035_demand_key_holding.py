# Generated by Django 3.1 on 2021-03-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0034_auto_20210314_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='key_holding',
            field=models.BooleanField(default=False, verbose_name='Key holding'),
        ),
    ]