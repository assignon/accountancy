# Generated by Django 3.1.5 on 2021-03-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20210320_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfers',
            name='brands',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='profiles',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='vehicle',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
