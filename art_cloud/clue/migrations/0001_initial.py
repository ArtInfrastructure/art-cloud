# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HelpText'
        db.create_table('clue_helptext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('rendered', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('clue', ['HelpText'])


    def backwards(self, orm):
        
        # Deleting model 'HelpText'
        db.delete_table('clue_helptext')


    models = {
        'clue.helptext': {
            'Meta': {'object_name': 'HelpText'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rendered': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['clue']
