# Generated by Django 3.1 on 2020-12-23 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditlog',
            name='object_type',
        ),
        migrations.AddField(
            model_name='auditlog',
            name='action_description',
            field=models.CharField(default='', max_length=256, null=True, verbose_name='Action Text'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='model_name',
            field=models.CharField(default='', max_length=256, null=True, verbose_name='Model Name'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='action',
            field=models.CharField(default='', max_length=256, null=True, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Agent'),
        ),
    ]