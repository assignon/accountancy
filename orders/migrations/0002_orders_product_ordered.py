# Generated by Django 3.1.5 on 2021-01-26 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='product_ordered',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.productordered'),
            preserve_default=False,
        ),
    ]
