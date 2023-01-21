# Generated by Django 3.1 on 2020-11-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20201106_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='type',
            field=models.CharField(choices=[('activity', 'Activity'), ('demand', 'Demand')], default='activity', max_length=20, null=True, verbose_name='Type'),
        ),
    ]