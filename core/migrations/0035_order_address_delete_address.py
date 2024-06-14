# Generated by Django 5.0.1 on 2024-03-24 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_remove_order_address_address'),
        ('userauths', '0019_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userauths.address'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
