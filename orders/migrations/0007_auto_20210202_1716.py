# Generated by Django 3.1.5 on 2021-02-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210130_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='email',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
