# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'HelpText', fields ['name']
        db.create_unique('clue_helptext', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'HelpText', fields ['name']
        db.delete_unique('clue_helptext', ['name'])


    models = {
        'clue.helptext': {
            'Meta': {'object_name': 'HelpText'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'rendered': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['clue']
