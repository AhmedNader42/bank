# Generated by Django 3.1.13 on 2021-08-12 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[('1', 'Banker'), ('2', 'CUSTOMER'), ('3', 'FUNDER')], default=2),
        ),
    ]
