# Generated by Django 4.1.5 on 2023-01-27 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_profile_ozon_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ozon_products',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='profile',
            name='wb_products',
            field=models.TextField(default='[]'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id_user',
            field=models.IntegerField(),
        ),
    ]