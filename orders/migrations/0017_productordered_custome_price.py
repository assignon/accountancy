# Generated by Django 3.1.5 on 2021-03-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_merge_20210305_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='productordered',
            name='custome_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]