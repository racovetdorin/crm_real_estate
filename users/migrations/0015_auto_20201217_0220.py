# Generated by Django 3.1 on 2020-12-17 02:20

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20201216_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AddField(
            model_name='user',
            name='user_settings',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('"darkMode":true', 'Dark Mode'), ('"leftSidebarCondensed":false', 'Condensed Sidebar')], max_length=44, null=True, verbose_name='User Settings'),
        ),
    ]
