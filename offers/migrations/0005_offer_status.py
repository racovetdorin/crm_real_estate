# Generated by Django 3.1 on 2020-11-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0004_auto_20201109_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('incomplete', 'Incomplete'), ('active', 'Active'), ('transacted', 'Transacted'), ('withdrawn', 'Withdrawn')], default='incomplete', max_length=50, verbose_name='Status'),
        ),
    ]
