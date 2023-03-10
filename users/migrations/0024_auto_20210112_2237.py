# Generated by Django 3.1 on 2021-01-12 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0011_officeimage_image_name'),
        ('users', '0023_userimage_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='offices.office', verbose_name='Office'),
        ),
    ]
