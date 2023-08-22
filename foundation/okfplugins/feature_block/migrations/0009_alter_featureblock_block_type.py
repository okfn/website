from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feature_block", "0008_alter_featureblock_cmsplugin_ptr"),
    ]

    operations = [
        migrations.AlterField(
            model_name="featureblock",
            name="block_type",
            field=models.CharField(
                choices=[
                    ("yellow_box", "Yellow Box"),
                    ("white_box", "White Box"),
                    ("transparent_title", "Transparent with Title"),
                    ("transparent_no_title", "Transparent without Title"),
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
