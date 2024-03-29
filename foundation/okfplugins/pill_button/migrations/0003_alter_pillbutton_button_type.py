# Generated by Django 3.2.16 on 2023-06-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pill_button", "0002_auto_20230627_1559"),
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
                    ("arrow", "Arrow"),
                ],
                default="pill",
                max_length=6,
            ),
        ),
    ]
