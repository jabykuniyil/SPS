# Generated by Django 3.1.7 on 2021-03-26 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_auto_20210325_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admin_approval',
            field=models.CharField(blank=True, default='pending', max_length=20, null=True),
        ),
    ]
