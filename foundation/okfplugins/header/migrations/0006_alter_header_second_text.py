# Generated by Django 4.2.3 on 2023-08-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("header", "0005_alter_header_cmsplugin_ptr"),
    ]

    operations = [
        migrations.AlterField(
            model_name="header",
            name="second_text",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="Highlight text"
            ),
        ),
    ]