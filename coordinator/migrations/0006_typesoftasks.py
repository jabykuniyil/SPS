# Generated by Django 3.1.7 on 2021-03-30 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0005_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypesOfTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal', models.TextField(blank=True, null=True)),
                ('technical', models.TextField(blank=True, null=True)),
                ('miscelleneous', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
