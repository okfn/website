# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BoardMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('board', models.ForeignKey(to='organisation.Board', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturedProject',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to='cms.CMSPlugin',
                    on_delete=models.CASCADE,
                )),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FeaturedTheme',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to='cms.CMSPlugin',
                    on_delete=models.CASCADE,
                )),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='NetworkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('group_type', models.IntegerField(default=0, choices=[(0, b'Local group'), (1, b'Chapter')])),
                ('description', models.TextField(null=True, blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('country_slug', models.SlugField()),
                ('region', models.CharField(max_length=100, blank=True)),
                ('region_slug', models.SlugField(default=None)),
                ('mailinglist_url', models.URLField(blank=True)),
                ('homepage_url', models.URLField(blank=True)),
                ('twitter', models.CharField(max_length=18, blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('gplus_url', models.URLField(verbose_name=b'Google+ url', blank=True)),
                ('wiki_url', models.URLField(blank=True)),
                ('position', models.CharField(max_length=42, null=True, blank=True)),
                ('extra_information', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('country', 'region'),
            },
        ),
        migrations.CreateModel(
            name='NetworkGroupList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to='cms.CMSPlugin',
                    on_delete=models.CASCADE,
                )),
                ('group_type', models.IntegerField(default=0, choices=[(0, b'Local group'), (1, b'Chapter')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='NetworkGroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('order', models.IntegerField(help_text=b'Higher numbers mean higher up in the food chain', null=True, blank=True)),
                ('networkgroup', models.ForeignKey(to='organisation.NetworkGroup', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-order', 'person__name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('photo', models.ImageField(upload_to=b'organisation/people/photos', blank=True)),
                ('twitter', models.CharField(max_length=18, blank=True)),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('teaser', models.CharField(help_text=b'A single line description for list views', max_length=100)),
                ('description', models.TextField()),
                ('banner', models.ImageField(help_text=b'A banner used for featuring this project on the front page', upload_to=b'projects/banners', blank=True)),
                ('picture', models.ImageField(help_text=b'A simple logo or picture to represent this project', upload_to=b'projects/pictures', blank=True)),
                ('twitter', models.CharField(max_length=18, blank=True)),
                ('homepage_url', models.URLField(blank=True)),
                ('sourcecode_url', models.URLField(blank=True)),
                ('mailinglist_url', models.URLField(blank=True)),
                ('featured', models.BooleanField(default=False, help_text=b'Should this be a featured project?')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProjectList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to='cms.CMSPlugin',
                    on_delete=models.CASCADE
                )),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SignupForm',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to='cms.CMSPlugin',
                    on_delete=models.CASCADE,
                )),
                ('title', models.CharField(default=b'Get Connected to Open Knowledge', max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('blurb', models.TextField(help_text=b'Blurb for theme page')),
                ('description', models.TextField()),
                ('picture', models.ImageField(help_text=b'A simple logo or picture to represent this theme', upload_to=b'themes/pictures', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField(help_text=b'Higher numbers mean higher up in the food chain', null=True, blank=True)),
            ],
            options={
                'ordering': ['-order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='UnitMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('order', models.IntegerField(help_text=b'Higher numbers mean higher up in the food chain', null=True, blank=True)),
                ('person', models.ForeignKey(to='organisation.Person', on_delete=models.CASCADE)),
                ('unit', models.ForeignKey(to='organisation.Unit', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-order', 'person__name'],
            },
        ),
        migrations.CreateModel(
            name='WorkingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField()),
                ('homepage_url', models.URLField(blank=True)),
                ('logo', models.ImageField(upload_to=b'organisation/working-groups/logos', blank=True)),
                ('incubation', models.BooleanField(default=True, help_text=b'Is this group in incubation?')),
                ('themes', models.ManyToManyField(related_name='workinggroups', to='organisation.Theme', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='unit',
            name='members',
            field=models.ManyToManyField(to='organisation.Person', through='organisation.UnitMembership'),
        ),
        migrations.AddField(
            model_name='projectlist',
            name='project_type',
            field=models.ForeignKey(
                blank=True,
                to='organisation.ProjectType',
                help_text=b'Limit to projects with this type',
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name='projectlist',
            name='theme',
            field=models.ForeignKey(
                blank=True,
                to='organisation.Theme',
                help_text=b'Limit to projects with this theme',
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='themes',
            field=models.ManyToManyField(to='organisation.Theme', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='types',
            field=models.ManyToManyField(to='organisation.ProjectType', blank=True),
        ),
        migrations.AddField(
            model_name='networkgroupmembership',
            name='person',
            field=models.ForeignKey(to='organisation.Person', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='networkgroup',
            name='members',
            field=models.ManyToManyField(to='organisation.Person', through='organisation.NetworkGroupMembership'),
        ),
        migrations.AddField(
            model_name='networkgroup',
            name='working_groups',
            field=models.ManyToManyField(to='organisation.WorkingGroup', blank=True),
        ),
        migrations.AddField(
            model_name='featuredtheme',
            name='theme',
            field=models.ForeignKey(
                related_name='+',
                to='organisation.Theme',
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name='featuredproject',
            name='project',
            field=models.ForeignKey(
                related_name='+',
                to='organisation.Project',
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name='boardmembership',
            name='person',
            field=models.ForeignKey(to='organisation.Person', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='board',
            name='members',
            field=models.ManyToManyField(to='organisation.Person', through='organisation.BoardMembership'),
        ),
        migrations.AlterUniqueTogether(
            name='networkgroup',
            unique_together=set([('country', 'region')]),
        ),
    ]
