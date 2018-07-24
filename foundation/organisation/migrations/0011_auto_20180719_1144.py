# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0010_networkgroup_forum_group_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardmembership',
            options={'ordering': ['-order', 'person__name']},
        ),
        migrations.AddField(
            model_name='boardmembership',
            name='order',
            field=models.IntegerField(help_text=b'Higher numbers mean higher up in the list', null=True, blank=True),
        ),
    ]
