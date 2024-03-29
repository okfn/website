# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Header",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="cms.CMSPlugin",
                        on_delete=models.CASCADE,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("text", models.CharField(max_length=200)),
                ("image", models.ImageField(upload_to=b"features/images")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
