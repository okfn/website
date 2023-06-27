# Generated by Django 3.2.16 on 2023-06-27 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pill_button", "0003_alter_pillbutton_button_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pillbutton",
            name="button_type",
            field=models.CharField(
                choices=[
                    ("black", "Black"),
                    ("white", "White"),
                    ("pill", "Pill"),
                    ("subtitle", "Subtitle"),
                    ("subtitle_large", "Subtitle large"),
                    ("arrow", "Arrow"),
                ],
                default="pill",
                max_length=16,
            ),
        ),
    ]
