# Generated by Django 3.2.16 on 2023-06-01 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heading', '0002_auto_20230601_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heading',
            name='highlighted',
            field=models.BooleanField(default=False),
        ),
    ]
