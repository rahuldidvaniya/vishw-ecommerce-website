# Generated by Django 5.0.1 on 2024-01-29 18:14

import core.models
import django.db.models.deletion
import django.utils.timezone
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_products_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='FeatureProduct',
        ),
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name_plural': 'Feature Products'},
        ),
        migrations.AddField(
            model_name='tags',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
        migrations.AddField(
            model_name='tags',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tags',
            name='description',
            field=models.TextField(blank=True, default='This is a product', null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='digital',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tags',
            name='image',
            field=models.ImageField(default='product.jpg', upload_to=core.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='tags',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='old_price',
            field=models.CharField(default='1.99', max_length=20),
        ),
        migrations.AddField(
            model_name='tags',
            name='pid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='', unique=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='price',
            field=models.CharField(default='1.99', max_length=20),
        ),
        migrations.AddField(
            model_name='tags',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('in_review', 'In Review'), ('published', 'Published')], default='in_review', max_length=10),
        ),
        migrations.AddField(
            model_name='tags',
            name='sale',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tags',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=10, prefix='sku', unique=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='specifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='title',
            field=models.CharField(default='TV', max_length=100),
        ),
        migrations.AddField(
            model_name='tags',
            name='updated',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p_images', to='core.products'),
        ),
        migrations.DeleteModel(
            name='FeatureProducts',
        ),
    ]
