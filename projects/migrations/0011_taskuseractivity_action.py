# Generated by Django 3.1.3 on 2021-02-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20210218_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskuseractivity',
            name='action',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
