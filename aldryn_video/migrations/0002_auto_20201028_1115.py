# Generated by Django 2.2.16 on 2020-10-28 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oembedvideoplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aldryn_video_oembedvideoplugin', serialize=False, to='cms.CMSPlugin'),
        ),
    ]
