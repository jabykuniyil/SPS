# Generated by Django 3.1.7 on 2021-04-03 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0011_remove_task_answer'),
        ('student', '0020_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.batches'),
        ),
    ]
