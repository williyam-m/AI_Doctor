# Generated by Django 5.0.7 on 2024-07-14 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('chat_name', models.CharField(max_length=200)),
                ('message', models.JSONField()),
                ('craeted_date', models.DateField(default=datetime.date(2024, 7, 14))),
            ],
        ),
    ]
