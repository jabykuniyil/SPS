# Generated by Django 3.1.7 on 2021-03-23 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_cautiondeposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='cautiondeposit',
            name='payment_mode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]