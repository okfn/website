# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PressRelease'
        db.create_table(u'press_pressrelease', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'press', ['PressRelease'])

        # Adding model 'PressMention'
        db.create_table(u'press_pressmention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('publication_date', self.gf('django.db.models.fields.DateField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'press', ['PressMention'])


    def backwards(self, orm):
        # Deleting model 'PressRelease'
        db.delete_table(u'press_pressrelease')

        # Deleting model 'PressMention'
        db.delete_table(u'press_pressmention')


    models = {
        u'press.pressmention': {
            'Meta': {'ordering': "('-publication_date',)", 'object_name': 'PressMention'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'press.pressrelease': {
            'Meta': {'ordering': "('-release_date',)", 'object_name': 'PressRelease'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['press']