# Generated by Django 5.0.7 on 2024-07-14 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='craeted_date',
            new_name='created_date',
        ),
    ]
