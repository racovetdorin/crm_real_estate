# Generated by Django 3.1 on 2020-09-28 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_delete_multiplezoneslocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='city',
            name='type',
            field=models.CharField(blank=True, choices=[('city', 'City'), ('village', 'Village')], db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='street',
            name='name',
            field=models.CharField(blank=True, max_length=256, verbose_name='Nume'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='name',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
