# Generated by Django 3.1.5 on 2021-01-30 19:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210130_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='start',
            field=models.DateField(default=datetime.datetime(2021, 1, 30, 19, 24, 11, 936088, tzinfo=utc)),
        ),
    ]