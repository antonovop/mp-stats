# Generated by Django 4.1.5 on 2023-01-24 17:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='api_ozon',
            new_name='ozon_keywords',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='api_wb',
            new_name='wb_keywords',
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]
