# Generated by Django 3.1.13 on 2021-08-20 11:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0030_auto_20210820_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='started',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
