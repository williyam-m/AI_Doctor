# Generated by Django 5.0.7 on 2024-10-04 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]