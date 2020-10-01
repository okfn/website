# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__latest__'),
        ('contenttypes', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OEmbedVideoPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('url', models.URLField(help_text='vimeo and youtube supported.', max_length=100, verbose_name='URL')),
                ('width', models.IntegerField(null=True, verbose_name='Width', blank=True)),
                ('height', models.IntegerField(null=True, verbose_name='Height', blank=True)),
                ('iframe_width', models.CharField(max_length=15, verbose_name='iframe width', blank=True)),
                ('iframe_height', models.CharField(max_length=15, verbose_name='iframe height', blank=True)),
                ('auto_play', models.BooleanField(default=False, verbose_name='auto play')),
                ('loop_video', models.BooleanField(default=False, help_text='when true, the video repeats itself when over.', verbose_name='loop')),
                ('oembed_data', jsonfield.fields.JSONField(null=True)),
                ('custom_params', models.CharField(help_text='define custom params (e.g. "start=10&end=50")', max_length=200, verbose_name='custom params', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
