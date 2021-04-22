# Generated by Django 3.1.7 on 2021-04-22 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0020_auto_20210420_1700'),
        ('student', '0032_reviewconducted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewconducted',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewconducted',
            name='week',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coordinator.week'),
        ),
    ]
