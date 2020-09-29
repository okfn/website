# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_sidebarextension'),
    ]

    operations = [
        migrations.CreateModel(
            name='NowDoing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doing_type', models.CharField(max_length=10, choices=[(b'reading', b'reading'), (b'listening', b'listening'), (b'working', b'working'), (b'location', b'location'), (b'watching', b'watching'), (b'eating', b'eating')])),
                ('link', models.URLField(null=True, blank=True)),
                ('text', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='username_on_slack',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='nowdoing',
            name='person',
            field=models.ForeignKey(to='organisation.Person', on_delete=models.CASCADE),
        ),
    ]
