# Generated by Django 3.1 on 2020-11-23 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0019_auto_20201116_1245'),
        ('activities', '0008_activity_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='demand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='demands.demand'),
        ),
    ]
