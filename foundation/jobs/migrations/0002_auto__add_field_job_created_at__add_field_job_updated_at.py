# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Job.created_at'
        db.add_column(u'jobs_job', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 6, 5, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Job.updated_at'
        db.add_column(u'jobs_job', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 6, 5, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Job.created_at'
        db.delete_column(u'jobs_job', 'created_at')

        # Deleting field 'Job.updated_at'
        db.delete_column(u'jobs_job', 'updated_at')


    models = {
        u'jobs.job': {
            'Meta': {'ordering': "('submission_closes',)", 'object_name': 'Job'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission_closes': ('django.db.models.fields.DateTimeField', [], {}),
            'submission_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['jobs']