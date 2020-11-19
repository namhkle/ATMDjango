# Generated by Django 3.1.3 on 2020-11-19 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_number', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('phone_number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ATM_Machine',
            fields=[
                ('atm_uid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('address', models.CharField(default='Group 1', max_length=30)),
                ('status', models.CharField(default='Active', max_length=30)),
                ('balance', models.PositiveIntegerField()),
                ('min_enquiry', models.PositiveIntegerField()),
                ('last_refill', models.DateField()),
                ('next_refill', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('card_number', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('pin', models.PositiveIntegerField(default=False)),
                ('card_name', models.CharField(max_length=30)),
                ('issue_date', models.DateField()),
                ('exp_date', models.DateField(default=datetime.datetime(2023, 11, 19, 15, 14, 38, 417010))),
                ('balance', models.PositiveIntegerField()),
                ('address', models.CharField(max_length=60)),
                ('phone_number', models.PositiveIntegerField()),
                ('status', models.CharField(default='Active', max_length=30)),
                ('transaction_history', models.TextField(blank=True)),
            ],
        ),
    ]
