# Generated by Django 3.1.7 on 2021-03-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_auto_20210325_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]