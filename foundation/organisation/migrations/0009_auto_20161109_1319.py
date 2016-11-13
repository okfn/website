# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0008_auto_20160707_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkgroup',
            name='group_type',
            field=models.IntegerField(default=0, choices=[(0, b'Local group'), (1, b'Chapter'), (2, b'Established group'), (3, b'Incubating group'), (4, b'Hibernated group'), (5, b'Affiliate')]),
        ),
        migrations.AlterField(
            model_name='networkgrouplist',
            name='group_type',
            field=models.IntegerField(default=0, choices=[(0, b'Local group'), (1, b'Chapter'), (2, b'Established group'), (3, b'Incubating group'), (4, b'Hibernated group'), (5, b'Affiliate')]),
        ),
    ]
