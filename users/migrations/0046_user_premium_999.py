# Generated by Django 3.1 on 2022-06-29 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_auto_20220510_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='premium_999',
            field=models.BooleanField(default=False, verbose_name='Premium account 999'),
        ),
    ]
