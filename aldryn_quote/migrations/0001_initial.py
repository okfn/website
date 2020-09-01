# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('style', models.CharField(default=b'standard', max_length=50, verbose_name='Style', choices=[(b'standard', 'Standard')])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('content', models.TextField(default=b'', verbose_name='Quote')),
                ('footer', models.TextField(verbose_name='Footer', blank=True)),
                ('url', models.URLField(verbose_name='Link', blank=True)),
                ('target', models.CharField(default=b'_blank', max_length=50, verbose_name='Target', blank=True, choices=[(b'_blank', 'New window')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
