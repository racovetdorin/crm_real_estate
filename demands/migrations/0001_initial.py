# Generated by Django 3.1 on 2020-09-15 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0003_auto_20200915_0613'),
        ('clients', '0004_auto_20200914_0643'),
        ('offices', '0002_office_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('sale', 'Sale'), ('rent', 'Rent')], max_length=56)),
                ('contract_number', models.CharField(blank=True, max_length=70)),
                ('contract_type', models.CharField(blank=True, max_length=70)),
                ('price_max', models.IntegerField(null=True)),
                ('price_min', models.IntegerField(null=True)),
                ('surface_min', models.FloatField(null=True)),
                ('surface_max', models.FloatField(null=True)),
                ('rooms_min', models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9)], null=True)),
                ('rooms_max', models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9)], null=True)),
                ('limit_date', models.DateTimeField(null=True)),
                ('comments', models.TextField(blank=True, max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to='clients.client')),
                ('location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.multiplezoneslocation')),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to='offices.office')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
