# Generated by Django 3.2.16 on 2023-06-16 08:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("image", "0003_okimage_show_caption"),
    ]

    operations = [
        migrations.AddField(
            model_name="okimage",
            name="in_gallery",
            field=models.BooleanField(default=False),
        ),
    ]
