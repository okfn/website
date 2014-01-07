# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'jobs_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('submission_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('submission_closes', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'jobs', ['Job'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'jobs_job')


    models = {
        u'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission_closes': ('django.db.models.fields.DateTimeField', [], {}),
            'submission_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['jobs']