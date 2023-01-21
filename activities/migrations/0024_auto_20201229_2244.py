# Generated by Django 3.1 on 2020-12-29 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0023_auto_20201229_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AddField(
            model_name='activity',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Deleted At'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
    ]