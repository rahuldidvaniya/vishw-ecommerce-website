# Generated by Django 5.0.1 on 2024-01-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='tags',
        ),
        migrations.AddField(
            model_name='products',
            name='sale',
            field=models.BooleanField(default=False),
        ),
    ]
