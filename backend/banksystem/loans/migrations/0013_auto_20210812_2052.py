# Generated by Django 3.1.13 on 2021-08-12 18:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0012_auto_20210812_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='started',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 18, 52, 58, 681173, tzinfo=utc)),
        ),
    ]
