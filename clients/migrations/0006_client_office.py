# Generated by Django 3.1 on 2020-09-17 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0002_office_deleted'),
        ('clients', '0005_auto_20200917_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='offices.office'),
        ),
    ]
