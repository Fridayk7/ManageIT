# Generated by Django 3.1.3 on 2021-04-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20210420_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='wbs',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
