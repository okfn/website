# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0007_add_old_project_bool_to_project_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkgroupmembership',
            name='order',
            field=models.IntegerField(help_text=b'The lower the number the higher on the page this Person will be shown.', null=True, blank=True),
        ),
    ]
