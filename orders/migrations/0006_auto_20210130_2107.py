# Generated by Django 3.1.5 on 2021-01-30 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210130_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='start',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='customers',
            name='times',
            field=models.IntegerField(),
        ),
    ]