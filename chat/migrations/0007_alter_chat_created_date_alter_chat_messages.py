# Generated by Django 5.0.7 on 2024-07-14 14:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_chat_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.JSONField(default=list),
        ),
    ]
