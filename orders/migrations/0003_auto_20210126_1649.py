# Generated by Django 3.1.5 on 2021-01-26 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_tires_quantity'),
        ('orders', '0002_orders_product_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='product_ordered',
        ),
        migrations.AddField(
            model_name='orders',
            name='product_ordered',
            field=models.ManyToManyField(to='orders.ProductOrdered'),
        ),
        migrations.RemoveField(
            model_name='productordered',
            name='product',
        ),
        migrations.AddField(
            model_name='productordered',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='products.tires'),
            preserve_default=False,
        ),
    ]