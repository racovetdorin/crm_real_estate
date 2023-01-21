# Generated by Django 3.1 on 2021-01-02 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_auto_20201216_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='is_agency',
            field=models.BooleanField(default=False, verbose_name='Is agency'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]