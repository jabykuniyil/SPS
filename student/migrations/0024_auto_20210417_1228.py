# Generated by Django 3.1.7 on 2021-04-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0023_answer_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
