# Generated by Django 3.1.7 on 2021-04-19 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0014_remove_task_batch'),
        ('student', '0026_auto_20210417_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='coordintator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coordinator.coordinatordetails'),
        ),
    ]
