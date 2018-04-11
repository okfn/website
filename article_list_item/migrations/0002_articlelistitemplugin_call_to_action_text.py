# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_list_item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistitemplugin',
            name='call_to_action_text',
            field=models.CharField(default='button text', max_length=100),
            preserve_default=False,
        ),
    ]
