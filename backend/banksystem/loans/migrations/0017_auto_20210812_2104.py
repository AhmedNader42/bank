# Generated by Django 3.1.13 on 2021-08-12 19:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0016_auto_20210812_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='started',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 19, 4, 8, 88607, tzinfo=utc)),
        ),
    ]
