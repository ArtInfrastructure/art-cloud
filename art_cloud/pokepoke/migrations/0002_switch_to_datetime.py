
from south.db import db
from django.db import models
from art_cloud.pokepoke.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'AlertLog.created'
        # (to signature: django.db.models.fields.DateTimeField(auto_now_add=True, blank=True))
        db.alter_column('pokepoke_alertlog', 'created', orm['pokepoke.alertlog:created'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'AlertLog.created'
        # (to signature: django.db.models.fields.DateField(auto_now_add=True, blank=True))
        db.alter_column('pokepoke_alertlog', 'created', orm['pokepoke.alertlog:created'])
        
    
    
    models = {
        'pokepoke.alertlog': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pokepoke.AlertPermission']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'pokepoke.alertpermission': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'FXdgEsbxYUMOocwfICSli14nth3zPem0r5kBaWRGpHZNQ97q28yu6vLJDjKVTA'", 'unique': 'True', 'max_length': '64'})
        }
    }
    
    complete_apps = ['pokepoke']
