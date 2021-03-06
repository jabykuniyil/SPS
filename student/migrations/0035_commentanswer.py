# Generated by Django 3.1.7 on 2021-04-30 06:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0021_coordinatordetails_status'),
        ('student', '0034_delete_reviewconducted'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.coordinatordetails')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.task')),
            ],
        ),
    ]
