# Generated by Django 3.2.16 on 2023-06-02 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullBanner',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='full_banner_fullbanner', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(max_length=200)),
                ('banner_background', models.ImageField(upload_to='video/images')),
                ('banner_text', models.CharField(default='', max_length=400)),
                ('banner_text_strong', models.CharField(default='', max_length=400)),
                ('banner_alt', models.CharField(default='', max_length=400)),
                ('banner_button_text', models.CharField(default='', max_length=400)),
                ('banner_link', models.CharField(default='', max_length=400)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
