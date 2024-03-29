# Generated by Django 3.2.16 on 2023-06-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feature_block", "0006_alter_featureblock_block_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="featureblock",
            name="block_type",
            field=models.CharField(
                choices=[
                    ("yellow", "Yellow"),
                    ("white", "White"),
                    ("transparent_title", "Transparent with Title"),
                    ("transparent", "Transparent"),
                    ("background_rounded", "Rounded corners"),
                    ("blue", "Blue Background"),
                    ("yellow", "Yellow Background"),
                    ("purple", "Purple Background"),
                ],
                default="yellow",
                max_length=20,
            ),
        ),
    ]
