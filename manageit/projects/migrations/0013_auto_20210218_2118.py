# Generated by Django 3.1.3 on 2021-02-18 21:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20210218_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskuseractivity',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
