# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HoneypotLog.from_url'
        db.add_column('django_honeypot_honeypotlog', 'from_url',
                      self.gf('django.db.models.fields.CharField')(default=None, null=True, max_length=1024),
                      keep_default=False)

        # Adding field 'HoneypotLog.request_url'
        db.add_column('django_honeypot_honeypotlog', 'request_url',
                      self.gf('django.db.models.fields.CharField')(default=None, null=True, max_length=1024),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HoneypotLog.from_url'
        db.delete_column('django_honeypot_honeypotlog', 'from_url')

        # Deleting field 'HoneypotLog.request_url'
        db.delete_column('django_honeypot_honeypotlog', 'request_url')


    models = {
        'django_honeypot.honeypotlog': {
            'Meta': {'object_name': 'HoneypotLog', 'ordering': "['created']"},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'null': 'True'}),
            'from_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'null': 'True', 'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_activity': ('django.db.models.fields.IntegerField', [], {'default': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'null': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'request_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'null': 'True', 'max_length': '1024'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['django_honeypot']