# Generated by Django 3.1.3 on 2020-11-16 10:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATM', '0005_auto_20201116_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='password',
            field=models.CharField(default=False, max_length=30),
        ),
        migrations.AlterField(
            model_name='card',
            name='exp_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 16, 5, 21, 25, 444564)),
        ),
    ]