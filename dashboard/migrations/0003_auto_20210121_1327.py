# Generated by Django 3.1.5 on 2021-01-21 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20210121_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='tires',
            old_name='name',
            new_name='size',
        ),
        migrations.AddField(
            model_name='tires',
            name='profiles',
            field=models.ManyToManyField(to='dashboard.Profiles'),
        ),
    ]
