# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0004_auto_20160616_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nowdoing',
            name='doing_type',
            field=models.CharField(max_length=10, choices=[(b'reading', b'reading'), (b'listening', b'listening'), (b'working', b'working'), (b'location', b'location'), (b'watching', b'watching'), (b'eating', b'eating')]),
        ),
    ]
