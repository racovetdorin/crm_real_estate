# Generated by Django 3.1 on 2021-01-29 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0028_auto_20210129_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='key_holding',
            field=models.BooleanField(default=False, verbose_name='Key holding'),
        ),
    ]
