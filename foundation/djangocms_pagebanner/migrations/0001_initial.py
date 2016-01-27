# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageBannerExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner_image', models.ImageField(upload_to=b'banners')),
                ('background_color', models.CharField(default=b'', max_length=50, blank=True)),
                ('font_color', models.CharField(default=b'', max_length=50, blank=True)),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='djangocms_pagebanner.PageBannerExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
