# Generated by Django 5.0.1 on 2024-02-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_rename_address_profile_address_business_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
