# Generated by Django 3.1 on 2020-11-17 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_auto_20201109_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='prefix_1',
            field=models.CharField(choices=[('+40', 'RO +40')], default='+40', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='prefix_2',
            field=models.CharField(choices=[('+40', 'RO +40')], default='+40', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='prefix_3',
            field=models.CharField(choices=[('+40', 'RO +40')], default='+40', max_length=20),
            preserve_default=False,
        ),
    ]
