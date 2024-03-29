# Generated by Django 3.1.3 on 2021-01-30 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='start',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='wbs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.wbs'),
        ),
        migrations.AlterField(
            model_name='wbs',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.wbs'),
        ),
    ]
