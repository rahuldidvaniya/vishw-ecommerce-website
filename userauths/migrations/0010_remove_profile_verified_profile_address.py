# Generated by Django 5.0.1 on 2024-02-20 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0009_user_activation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='verified',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
