# Generated by Django 3.1 on 2020-09-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0003_auto_20200923_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='demand',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]