# Generated by Django 3.1 on 2022-02-22 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_remove_user_rex_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='specialization',
            field=models.PositiveIntegerField(blank=True, default=1310, null=True, verbose_name='Specialization'),
        ),
    ]
