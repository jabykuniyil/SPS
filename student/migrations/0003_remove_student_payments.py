# Generated by Django 3.1.7 on 2021-03-23 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_payments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='payments',
        ),
    ]
