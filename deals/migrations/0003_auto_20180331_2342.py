# Generated by Django 2.0.3 on 2018-03-31 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_auto_20180330_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='url',
            field=models.URLField(max_length=2048, verbose_name='URL'),
        ),
    ]