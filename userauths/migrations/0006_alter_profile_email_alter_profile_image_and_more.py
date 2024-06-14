# Generated by Django 5.0.1 on 2024-02-16 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0005_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
