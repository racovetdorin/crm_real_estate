# Generated by Django 3.1 on 2022-10-10 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0046_user_premium_999'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('counselor', 'Real estate counselor'), ('managing_director', 'Managing director'), ('assistant_manager', 'Assistant manager'), ('secretariat', 'Secretariat'), ('it_administrator', 'IT Administrator'), ('specialist', 'Real estate specialist'), ('broker_owner', 'Broker owner'), ('marketing_manager', 'Marketing Manager'), ('mortage_broker', 'Mortage Broker'), ('office_manager', 'Office Manager')], max_length=256, null=True, verbose_name='Role'),
        ),
    ]