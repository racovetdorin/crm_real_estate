# Generated by Django 3.1 on 2021-10-26 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0047_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='mls_999',
            field=models.BooleanField(default=False, verbose_name='999.MD'),
        ),
        migrations.AddField(
            model_name='offer',
            name='mls_999_data',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='mls_remax_global',
            field=models.BooleanField(default=False, verbose_name='RE/MAX Global'),
        ),
        migrations.AddField(
            model_name='offer',
            name='mls_remax_global_data',
            field=models.JSONField(default=dict, null=True),
        ),
    ]