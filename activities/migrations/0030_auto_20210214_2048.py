# Generated by Django 3.1 on 2021-02-14 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0029_activity_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Deleted'),
        ),
    ]
