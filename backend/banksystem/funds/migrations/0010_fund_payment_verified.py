# Generated by Django 3.1.13 on 2021-08-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0009_auto_20210820_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='payment_verified',
            field=models.BooleanField(default=False),
        ),
    ]