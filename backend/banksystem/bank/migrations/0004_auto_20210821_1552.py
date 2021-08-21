# Generated by Django 3.1.13 on 2021-08-21 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='in_flow',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='bank',
            name='out_flow',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
    ]
