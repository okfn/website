# Generated by Django 4.2.3 on 2023-07-04 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0022_auto_20180620_1551"),
        ("hero_punch", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heropunch",
            name="cmsplugin_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name="%(app_label)s_%(class)s",
                serialize=False,
                to="cms.cmsplugin",
            ),
        ),
    ]
