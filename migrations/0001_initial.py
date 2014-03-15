# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HoneypotLog'
        db.create_table('django_honeypot_honeypotlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, auto_now=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('last_activity', self.gf('django.db.models.fields.IntegerField')(default=255)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_honeypot', ['HoneypotLog'])


    def backwards(self, orm):
        # Deleting model 'HoneypotLog'
        db.delete_table('django_honeypot_honeypotlog')


    models = {
        'django_honeypot.honeypotlog': {
            'Meta': {'object_name': 'HoneypotLog', 'ordering': "['created']"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_activity': ('django.db.models.fields.IntegerField', [], {'default': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['django_honeypot']