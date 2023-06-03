# Generated by Django 3.2.16 on 2023-06-03 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_block', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureblock',
            name='block_type',
            field=models.CharField(choices=[('yellow', 'Yellow'), ('white', 'White'), ('transparent', 'Transparent')], default='yellow', max_length=20),
        ),
        migrations.AddField(
            model_name='featureblock',
            name='image',
            field=models.ImageField(blank=True, upload_to='feature_block/images'),
        ),
    ]
