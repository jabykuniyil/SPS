# Generated by Django 3.1.7 on 2021-04-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0025_auto_20210417_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
