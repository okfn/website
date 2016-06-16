# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_auto_20160616_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nowdoing',
            name='link',
            field=models.URLField(null=True, blank=True),
        ),
    ]
