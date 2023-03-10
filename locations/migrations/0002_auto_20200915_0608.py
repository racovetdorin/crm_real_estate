# Generated by Django 3.1 on 2020-09-15 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('type', models.IntegerField(blank=True, choices=[('city', 'City'), ('village', 'Village')], db_index=True, null=True)),
            ],
            options={
                'verbose_name': 'Oraș',
                'verbose_name_plural': 'Orașe',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(blank=True, help_text='Codul țării (două caractere) in formatul ISO 3166-1', max_length=10)),
            ],
            options={
                'verbose_name': 'Țară',
                'verbose_name_plural': 'Țări',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='location',
            name='street',
            field=models.CharField(blank=True, max_length=256, verbose_name='Stradă'),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zones', to='locations.city')),
            ],
            options={
                'verbose_name': 'Zonă',
                'verbose_name_plural': 'Zone',
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nume')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='streets', to='locations.city', verbose_name='Oraș')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.zone', verbose_name='Zonă')),
            ],
            options={
                'verbose_name': 'Stradă',
                'verbose_name_plural': 'Străzi',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regions', to='locations.country')),
            ],
            options={
                'verbose_name': 'Județ',
                'verbose_name_plural': 'Județe',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MultipleZonesLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.city', verbose_name='Localitate')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.region', verbose_name='Județ')),
                ('zones', models.ManyToManyField(blank=True, null=True, to='locations.Zone', verbose_name='Zonă')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cities', to='locations.region'),
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.city', verbose_name='Localitate'),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.region', verbose_name='Județ'),
        ),
        migrations.AddField(
            model_name='location',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.zone', verbose_name='Zonă'),
        ),
    ]
