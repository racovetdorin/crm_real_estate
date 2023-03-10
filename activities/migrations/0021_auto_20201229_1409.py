# Generated by Django 3.1 on 2020-12-29 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_auto_20201228_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('to_do', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done'), ('sale', 'Sale Offers'), ('rent', 'Rent Offers'), ('processed', 'Processed')], default='', max_length=256, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(choices=[('viewing', 'Viewing'), ('virtual_viewing', 'Virtual Viewing'), ('demand_activity', 'Demand Activity'), ('property_lead_generation', 'Property Lead Generation'), ('client_lead_generation', 'Client Lead Generation'), ('telephone_conversation', 'Telephone Conversation'), ('photo_viewing', 'Photo Viewing')], default='', max_length=256, verbose_name='Type'),
        ),
    ]
