# Generated by Django 3.1.7 on 2021-04-17 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_auto_20210403_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
