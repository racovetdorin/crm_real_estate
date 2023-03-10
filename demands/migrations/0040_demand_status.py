# Generated by Django 3.1 on 2021-03-25 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0039_demand_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='status',
            field=models.CharField(blank=True, choices=[('prospect', 'Prospect'), ('contracted', 'Contracted'), ('transacted', 'Transacted by Impakt'), ('transacted_by_others', 'Transacted by others'), ('transacted_by_owner', 'Transacted by owner'), ('withdrawn', 'Withdrawn')], default='prospect', max_length=50, null=True, verbose_name='Status'),
        ),
    ]
