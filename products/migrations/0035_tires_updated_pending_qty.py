# Generated by Django 3.1.5 on 2021-04-27 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_auto_20210428_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='tires',
            name='updated_pending_qty',
            field=models.IntegerField(default=0),
        ),
    ]
