# Generated by Django 3.1 on 2021-01-29 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0011_officeimage_image_name'),
        ('users', '0024_auto_20210112_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='offices.office', verbose_name='Office'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Phone'),
        ),
    ]