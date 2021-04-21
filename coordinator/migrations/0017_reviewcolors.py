# Generated by Django 3.1.7 on 2021-04-19 07:33

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0016_delete_reviewcolors'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewColors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('green', colorfield.fields.ColorField(default='#13C60E', max_length=18)),
                ('yellow', colorfield.fields.ColorField(default='#E7F100', max_length=18)),
                ('orange', colorfield.fields.ColorField(default='#FF5733', max_length=18)),
                ('red', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
            ],
        ),
    ]
