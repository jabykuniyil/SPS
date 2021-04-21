# Generated by Django 3.1.7 on 2021-04-19 07:39

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0017_reviewcolors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewcolors',
            name='green',
        ),
        migrations.RemoveField(
            model_name='reviewcolors',
            name='orange',
        ),
        migrations.RemoveField(
            model_name='reviewcolors',
            name='red',
        ),
        migrations.RemoveField(
            model_name='reviewcolors',
            name='yellow',
        ),
        migrations.AddField(
            model_name='reviewcolors',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', max_length=18),
        ),
        migrations.AddField(
            model_name='reviewcolors',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
