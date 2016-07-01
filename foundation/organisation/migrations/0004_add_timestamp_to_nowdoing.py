# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_add_nowdoing_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='nowdoing',
            name='updated_at',
            # We need to set a default value for this new non nullable field so we just
            # take today's date
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 1, 8, 0, 0, 0, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
