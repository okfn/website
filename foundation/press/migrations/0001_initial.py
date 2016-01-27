# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PressMention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publisher', models.CharField(max_length=60)),
                ('publication_date', models.DateField()),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('notes', models.TextField()),
                ('published', models.BooleanField()),
            ],
            options={
                'ordering': ('-publication_date',),
            },
        ),
        migrations.CreateModel(
            name='PressRelease',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('body', models.TextField()),
                ('release_date', models.DateTimeField()),
            ],
            options={
                'ordering': ('-release_date',),
            },
        ),
    ]
