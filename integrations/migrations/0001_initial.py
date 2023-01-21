# Generated by Django 3.1 on 2022-02-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('access_key', models.CharField(blank=True, max_length=100, null=True, verbose_name='Access integration key')),
                ('refresh_token', models.CharField(blank=True, max_length=100, null=True, verbose_name='Refresh token')),
            ],
        ),
    ]
