# Generated by Django 3.1.7 on 2021-04-22 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0020_auto_20210420_1700'),
        ('student', '0031_auto_20210419_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewConducted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_review_conducted', models.BooleanField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.week')),
            ],
        ),
    ]