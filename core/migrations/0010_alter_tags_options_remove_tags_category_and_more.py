# Generated by Django 5.0.1 on 2024-01-30 13:21

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_products_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tags',
            options={},
        ),
        migrations.RemoveField(
            model_name='tags',
            name='category',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='date',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='digital',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='image',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='in_stock',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='old_price',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='pid',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='price',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='product_status',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='sku',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='specifications',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='status',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='title',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='user',
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='This is a product', null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='specifications',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]