# Generated by Django 3.1.5 on 2021-01-28 22:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='start',
            field=models.DateField(default=datetime.datetime(2021, 1, 28, 22, 56, 24, 351207, tzinfo=utc)),
        ),
    ]
