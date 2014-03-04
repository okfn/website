# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PressRelease.slug'
        db.alter_column(u'press_pressrelease', 'slug', self.gf('django.db.models.fields.SlugField')(default='nonunique', unique=True, max_length=100))
        # Adding unique constraint on 'PressRelease', fields ['slug']
        db.create_unique(u'press_pressrelease', ['slug'])


        # Changing field 'PressMention.slug'
        db.alter_column(u'press_pressmention', 'slug', self.gf('django.db.models.fields.SlugField')(default='nonunique', unique=True, max_length=100))
        # Adding unique constraint on 'PressMention', fields ['slug']
        db.create_unique(u'press_pressmention', ['slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'PressMention', fields ['slug']
        db.delete_unique(u'press_pressmention', ['slug'])

        # Removing unique constraint on 'PressRelease', fields ['slug']
        db.delete_unique(u'press_pressrelease', ['slug'])


        # Changing field 'PressRelease.slug'
        db.alter_column(u'press_pressrelease', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True))

        # Changing field 'PressMention.slug'
        db.alter_column(u'press_pressmention', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True))

    models = {
        u'press.pressmention': {
            'Meta': {'ordering': "('-publication_date',)", 'object_name': 'PressMention'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'press.pressrelease': {
            'Meta': {'ordering': "('-release_date',)", 'object_name': 'PressRelease'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['press']
