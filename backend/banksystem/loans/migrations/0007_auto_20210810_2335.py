# Generated by Django 3.1.13 on 2021-08-10 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0006_auto_20210810_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='started',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
