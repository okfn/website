# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0012_auto_20191204_1651'),
    ]

    operations = [
        migrations.RunSQL(
            sql=["UPDATE organisation_networkgroup SET country_slug='czechia' WHERE country_slug='czech-republic';"],
            reverse_sql=["UPDATE organisation_networkgroup SET country_slug='czech-republic' WHERE country_slug='czechia';"]
        ),
        migrations.RunSQL(
            sql=["UPDATE organisation_networkgroup SET country_slug='north-macedonia' WHERE country_slug='macedonia';"],
            reverse_sql=["UPDATE organisation_networkgroup SET country_slug='macedonia' WHERE country_slug='north-macedonia';"]
        )
    ]
