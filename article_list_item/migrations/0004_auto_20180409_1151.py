# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_list_item', '0003_auto_20180409_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistitemplugin',
            name='image',
            field=models.ImageField(upload_to=b'articles/thumbs', blank=True),
        ),
        migrations.AlterField(
            model_name='articlelistitemplugin',
            name='call_to_action_text',
            field=models.CharField(default=b'Read more', max_length=50, blank=True),
        ),
    ]
