# Generated by Django 3.1.13 on 2021-08-19 23:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0027_auto_20210813_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='payment_url',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='loan',
            name='started',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 19, 23, 17, 49, 537329, tzinfo=utc)),
        ),
    ]
