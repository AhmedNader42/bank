# Generated by Django 3.1.13 on 2021-08-12 21:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0002_auto_20210812_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='started',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 21, 5, 48, 862482, tzinfo=utc)),
        ),
    ]
