# Generated by Django 5.0.1 on 2024-03-21 19:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_order_discount_alter_order_sub_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AddField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]