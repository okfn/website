# Generated by Django 4.2.3 on 2023-07-17 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("organisation", "0020_remove_featuredtheme_cmsplugin_ptr_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Project",
        ),
        migrations.DeleteModel(
            name="ProjectType",
        ),
    ]
