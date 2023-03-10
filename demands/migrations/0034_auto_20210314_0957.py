# Generated by Django 3.1 on 2021-03-14 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0033_auto_20210304_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False, verbose_name='Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted At')),
                ('name', models.CharField(max_length=80, verbose_name='Source lead name')),
                ('slug', models.CharField(blank=True, max_length=80, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='demand',
            name='lead_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to='demands.leadsource', verbose_name='Lead source'),
        ),
    ]
