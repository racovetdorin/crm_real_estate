# Generated by Django 3.1 on 2022-02-22 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0039_auto_20220222_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='promote_rex',
            field=models.BooleanField(default=True, verbose_name='Promote Global'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_sale_associate',
            field=models.BooleanField(default=True, verbose_name='Is Sale associate'),
        ),
    ]