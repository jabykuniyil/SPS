# Generated by Django 3.1.7 on 2021-04-19 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0030_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='coordinator',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
