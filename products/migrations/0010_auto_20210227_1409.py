# Generated by Django 3.1.5 on 2021-02-27 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210227_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tires',
            name='vehicule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.vehicule'),
        ),
    ]