# Generated by Django 3.1.7 on 2021-04-20 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0019_auto_20210419_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewcolors',
            name='score_from',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reviewcolors',
            name='score_to',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
