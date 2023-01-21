# Generated by Django 3.1 on 2021-06-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0043_offer_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='withdrawn_reason',
            field=models.CharField(blank=True, choices=[('expired_contract', 'Expired contract'), ('cancelled_contract', 'Cancelled contract'), ('other', 'Other')], max_length=50, null=True, verbose_name='Withdrawn reason'),
        ),
    ]