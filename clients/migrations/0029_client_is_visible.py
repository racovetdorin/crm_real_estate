# Generated by Django 3.1 on 2022-02-11 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0028_auto_20220207_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_visible',
            field=models.BooleanField(default=False, verbose_name='Is visible'),
        ),
    ]
