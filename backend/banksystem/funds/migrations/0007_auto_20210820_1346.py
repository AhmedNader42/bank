# Generated by Django 3.1.13 on 2021-08-20 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0006_auto_20210820_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='payment_url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='fund',
            name='started',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
