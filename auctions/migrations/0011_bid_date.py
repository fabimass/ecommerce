# Generated by Django 4.1.6 on 2023-02-20 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_bid_bidded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 20, 14, 54, 30, 532358)),
        ),
    ]