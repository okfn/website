# Generated by Django 3.2.16 on 2023-06-29 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("image", "0005_okimage_text_black"),
    ]

    operations = [
        migrations.AddField(
            model_name="okimage",
            name="full_width",
            field=models.BooleanField(default=False),
        ),
    ]
