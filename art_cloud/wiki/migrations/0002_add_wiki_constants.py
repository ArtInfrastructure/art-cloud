
from south.db import db
from django.db import models
from art_cloud.wiki.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'WikiConstant'
        db.create_table('wiki_wikiconstant', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=512, null=False, blank=False)),
            ('constant', models.TextField(null=False, blank=False)),
        ))
        db.send_create_signal('wiki', ['WikiConstant'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'WikiConstant'
        db.delete_table('wiki_wikiconstant')
        
    
    
    models = {
        'wiki.wikiphoto': {
            'Meta': {'ordering': "['-created']"},
            'caption': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {'blank': 'False'}),
            'title': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('models.ForeignKey', ["orm['wiki.WikiPage']"], {'null': 'False', 'blank': 'False'})
        },
        'wiki.wikifile': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('models.FileField', [], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('models.ForeignKey', ["orm['wiki.WikiPage']"], {'null': 'False', 'blank': 'False'})
        },
        'wiki.wikiconstant': {
            'constant': ('models.TextField', [], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '512', 'null': 'False', 'blank': 'False'})
        },
        'wiki.wikipage': {
            'Meta': {'ordering': "('name',)"},
            'content': ('models.TextField', [], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'rendered': ('models.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'wiki.wikipagelog': {
            'Meta': {'ordering': "('-created',)"},
            'content': ('models.TextField', [], {'null': 'False', 'blank': 'False'}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'wiki_page': ('models.ForeignKey', ["orm['wiki.WikiPage']"], {'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['wiki']
