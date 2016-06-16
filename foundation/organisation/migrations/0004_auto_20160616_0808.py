# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_auto_20160615_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='NowDoing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doing_type', models.CharField(max_length=10, choices=[(b'READING', b'reading'), (b'LISTENING', b'listening'), (b'WORKING', b'working')])),
                ('link', models.URLField(blank=True)),
                ('text', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='now_reading',
        ),
        migrations.AddField(
            model_name='nowdoing',
            name='person',
            field=models.ForeignKey(to='organisation.Person'),
        ),
    ]
