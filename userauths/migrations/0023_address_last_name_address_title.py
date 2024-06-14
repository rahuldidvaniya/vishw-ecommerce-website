# Generated by Django 5.0.1 on 2024-04-08 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0022_remove_address_last_name_remove_address_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='address',
            name='title',
            field=models.CharField(choices=[('home', 'Home'), ('office', 'Office'), ('business', 'Business')], max_length=10, null=True),
        ),
    ]