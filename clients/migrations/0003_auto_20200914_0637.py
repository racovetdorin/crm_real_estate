# Generated by Django 3.1 on 2020-09-14 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0002_auto_20200914_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]