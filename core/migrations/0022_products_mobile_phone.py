# Generated by Django 5.0.1 on 2024-02-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_products_televisions_remove_products_laptops_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='mobile_phone',
            field=models.BooleanField(default=False),
        ),
    ]