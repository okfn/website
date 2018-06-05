# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_list_item', '0002_articlelistitemplugin_call_to_action_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistitemplugin',
            name='call_to_action_url',
            field=models.URLField(default='#'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articlelistitemplugin',
            name='call_to_action_text',
            field=models.CharField(default=b'Read more', max_length=50),
        ),
    ]
