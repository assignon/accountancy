# Generated by Django 3.1.5 on 2021-02-15 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20210215_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_status',
            name='payed',
            field=models.BooleanField(default=False),
        ),
    ]
