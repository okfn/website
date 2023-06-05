# Generated by Django 3.2.16 on 2023-06-02 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('full_banner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullbanner',
            name='banner_picture',
            field=models.ImageField(blank=True, upload_to='banner/images'),
        ),
        migrations.AlterField(
            model_name='fullbanner',
            name='banner_background',
            field=models.ImageField(blank=True, upload_to='banner/images'),
        ),
    ]