# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Job',
        ),
    ]
