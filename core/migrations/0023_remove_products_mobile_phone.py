# Generated by Django 5.0.1 on 2024-02-27 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_products_mobile_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='mobile_phone',
        ),
    ]
