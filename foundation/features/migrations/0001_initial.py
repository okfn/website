# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=b'features/images')),
                ('link', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'features',
            },
        ),
    ]
