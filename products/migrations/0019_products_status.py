# Generated by Django 3.1.5 on 2021-04-23 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20210423_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]
