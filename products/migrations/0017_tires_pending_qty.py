# Generated by Django 3.1.5 on 2021-04-22 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_transfers_sender_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tires',
            name='pending_qty',
            field=models.IntegerField(default=0),
        ),
    ]