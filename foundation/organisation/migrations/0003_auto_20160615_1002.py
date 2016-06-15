# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_sidebarextension'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='now_reading',
            field=models.CharField(max_length=140, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='username_on_slack',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
