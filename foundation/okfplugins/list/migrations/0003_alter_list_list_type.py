# Generated by Django 4.2.3 on 2023-08-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("list", "0002_alter_list_cmsplugin_ptr"),
    ]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="list_type",
            field=models.CharField(
                choices=[("long", "Long"), ("short", "Short"), ("xl", "XL no title")],
                default="long",
                max_length=6,
            ),
        ),
    ]
