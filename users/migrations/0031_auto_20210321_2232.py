# Generated by Django 3.1 on 2021-03-21 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_user_show_on_site'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['position_on_site']},
        ),
        migrations.AddField(
            model_name='user',
            name='position_on_site',
            field=models.IntegerField(default=999999),
        ),
    ]
