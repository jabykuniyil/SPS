# Generated by Django 3.1.7 on 2021-03-29 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0004_auto_20210329_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, null=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.batches')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.week')),
            ],
        ),
    ]
