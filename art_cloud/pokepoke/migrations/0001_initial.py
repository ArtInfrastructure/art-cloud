
from south.db import db
from django.db import models
from art_cloud.pokepoke.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AlertPermission'
        db.create_table('pokepoke_alertpermission', (
            ('id', orm['pokepoke.AlertPermission:id']),
            ('name', orm['pokepoke.AlertPermission:name']),
            ('secret', orm['pokepoke.AlertPermission:secret']),
        ))
        db.send_create_signal('pokepoke', ['AlertPermission'])
        
        # Adding model 'AlertLog'
        db.create_table('pokepoke_alertlog', (
            ('id', orm['pokepoke.AlertLog:id']),
            ('created', orm['pokepoke.AlertLog:created']),
            ('permission', orm['pokepoke.AlertLog:permission']),
            ('message', orm['pokepoke.AlertLog:message']),
        ))
        db.send_create_signal('pokepoke', ['AlertLog'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AlertPermission'
        db.delete_table('pokepoke_alertpermission')
        
        # Deleting model 'AlertLog'
        db.delete_table('pokepoke_alertlog')
        
    
    
    models = {
        'pokepoke.alertlog': {
            'created': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pokepoke.AlertPermission']"})
        },
        'pokepoke.alertpermission': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'create_secret'", 'max_length': '64'})
        }
    }
    
    complete_apps = ['pokepoke']
