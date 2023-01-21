# Generated by Django 3.1 on 2020-09-14 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='email_home',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='email_work',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='is_agency',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='phone_home',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='phone_work',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
