# Generated by Django 5.0.1 on 2024-02-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_products_link_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='banner_image',
            field=models.ImageField(default='brand.jpg', upload_to='brand'),
        ),
    ]
