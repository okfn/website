# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0009_auto_20161109_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkgroup',
            name='forum_group_url',
            field=models.URLField(blank=True),
        ),
    ]
