# Generated by Django 3.1 on 2022-03-02 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0053_auto_20220302_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='mls_999',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='999.MD'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='mls_999_data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]