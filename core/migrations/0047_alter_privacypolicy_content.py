# Generated by Django 5.0.1 on 2024-04-17 14:11

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_privacypolicy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypolicy',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]