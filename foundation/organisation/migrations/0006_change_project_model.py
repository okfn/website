# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_add_timestamp_to_nowdoing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='banner',
        ),
        migrations.RemoveField(
            model_name='project',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='project',
            name='mailinglist_url',
        ),
        migrations.AddField(
            model_name='project',
            name='forum_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='teaser',
            field=models.CharField(help_text=b'A single line description for list views', max_length=400),
        ),
    ]
