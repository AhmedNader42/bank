# Generated by Django 3.1.13 on 2021-08-12 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'banker'), (2, 'customer'), (3, 'funder')]),
        ),
    ]
