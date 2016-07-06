# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0006_change_project_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='old_project',
            field=models.BooleanField(default=False, help_text=b'Is this an old/archived project?'),
        ),
    ]
