# Generated by Django 3.1.5 on 2021-02-26 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_tires_warehouse_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tires',
            name='brands_str',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tires',
            name='profiles_str',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
