# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_add_nowdoing_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='networkgroup',
            name='gplus_url',
        ),
        migrations.RemoveField(
            model_name='networkgroup',
            name='wiki_url',
        ),
        migrations.RemoveField(
            model_name='networkgroup',
            name='youtube_url',
        ),
    ]
