# Generated by Django 3.1.7 on 2021-04-16 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0012_auto_20210412_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coordinator.batches'),
        ),
    ]