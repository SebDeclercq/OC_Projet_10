# Generated by Django 2.1.7 on 2019-04-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0004_auto_20190322_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.URLField(blank=True, verbose_name='img'),
        ),
        migrations.AddField(
            model_name='product',
            name='nutrition_img',
            field=models.URLField(blank=True, verbose_name='nutrition_img'),
        ),
    ]
