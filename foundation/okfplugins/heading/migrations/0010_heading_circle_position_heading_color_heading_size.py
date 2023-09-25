# Generated by Django 4.2.3 on 2023-08-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("heading", "0009_remove_heading_is_anchor"),
    ]

    operations = [
        migrations.AddField(
            model_name="heading",
            name="circle_position",
            field=models.CharField(
                blank=True,
                choices=[
                    ("default", "Default"),
                    ("right", "Right"),
                    ("top_left", "Top Left"),
                    ("top_right", "Top Right"),
                    ("bottom_left", "Bottom Left"),
                    ("bottom_right", "Bottom Right"),
                ],
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="heading",
            name="color",
            field=models.CharField(
                blank=True,
                choices=[
                    ("-bg-circle-okfn-yellow", "Yellow"),
                    ("-bg-circle-okfn-green", "Green"),
                    ("-bg-circle-okfn-purple", "Purple"),
                ],
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="heading",
            name="size",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Default"),
                    ("-bg-circle-sm", "Small"),
                    ("-bg-circle-lg", "Large"),
                    ("-bg-circle-xs", "Extra Small"),
                    ("-bg-circle-full", "Full"),
                ],
                max_length=30,
            ),
        ),
    ]