# Generated by Django 5.0.1 on 2024-02-17 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_profile_secondary_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]