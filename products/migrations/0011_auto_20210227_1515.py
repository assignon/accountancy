# Generated by Django 3.1.5 on 2021-02-27 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210227_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tires',
            options={'ordering': ['-id']},
        ),
    ]
