# Generated by Django 5.0.1 on 2024-03-20 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0012_alter_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='full_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
