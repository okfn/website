# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_list_item', '0004_auto_20180409_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlelistitemplugin',
            name='call_to_action_url',
            field=models.CharField(max_length=100),
        ),
    ]
