# Generated by Django 3.1 on 2020-11-26 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0004_auto_20201106_1534'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offers', '0005_offer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='commission',
            field=models.IntegerField(default=100, verbose_name='Commission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='commission_percent',
            field=models.IntegerField(default=100, verbose_name='Commission %'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='final_price',
            field=models.IntegerField(default=100, verbose_name='Final Price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='is_transacted',
            field=models.BooleanField(default=False, verbose_name='Is Transacted'),
        ),
        migrations.AddField(
            model_name='offer',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='offices.office'),
        ),
        migrations.AddField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]