# Generated by Django 3.1.13 on 2021-08-12 22:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0025_auto_20210812_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='loan_type',
            new_name='option',
        ),
        migrations.AlterField(
            model_name='loan',
            name='started',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 22, 27, 14, 222455, tzinfo=utc)),
        ),
    ]
