# Generated by Django 3.2.16 on 2023-06-29 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cms", "0022_auto_20180620_1551"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="quote_quote",
                        serialize=False,
                        to="cms.cmsplugin",
                    ),
                ),
                ("text", models.CharField(max_length=500)),
                ("author", models.CharField(blank=True, max_length=200)),
                (
                    "alignment",
                    models.CharField(
                        choices=[("center", "Center"), ("left", "Left")],
                        default="center",
                        max_length=6,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("cms.cmsplugin",),
        ),
    ]
