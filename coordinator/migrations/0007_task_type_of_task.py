# Generated by Django 3.1.7 on 2021-03-30 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0006_typesoftasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='type_of_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coordinator.typesoftasks'),
        ),
    ]
