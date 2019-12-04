# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0011_auto_20180719_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='order',
            field=models.IntegerField(help_text=b'Higher numbers mean higher up in the list', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='unitmembership',
            name='order',
            field=models.IntegerField(help_text=b'Higher numbers mean higher up in the list', null=True, blank=True),
        ),
    ]
