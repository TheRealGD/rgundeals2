# Generated by Django 2.0.3 on 2018-04-01 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0003_auto_20180331_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='url',
            field=models.URLField(max_length=4096, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]