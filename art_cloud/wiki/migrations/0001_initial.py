
from south.db import db
from django.db import models
from art_cloud.wiki.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'WikiPhoto'
        db.create_table('wiki_wikiphoto', (
            ('description', models.TextField(null=True, blank=True)),
            ('title', models.CharField(max_length=1024, null=True, blank=True)),
            ('image', models.ImageField(blank=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('caption', models.CharField(max_length=1024, null=True, blank=True)),
            ('wiki_page', models.ForeignKey(orm.WikiPage, null=False, blank=False)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('wiki', ['WikiPhoto'])
        
        # Adding model 'WikiFile'
        db.create_table('wiki_wikifile', (
            ('description', models.TextField(null=True, blank=True)),
            ('title', models.CharField(max_length=1024, null=True, blank=True)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('file', models.FileField(null=False, blank=False)),
            ('wiki_page', models.ForeignKey(orm.WikiPage, null=False, blank=False)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('wiki', ['WikiFile'])
        
        # Adding model 'WikiPage'
        db.create_table('wiki_wikipage', (
            ('content', models.TextField(null=False, blank=False)),
            ('rendered', models.TextField(null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(unique=True, max_length=255, null=False, blank=False)),
        ))
        db.send_create_signal('wiki', ['WikiPage'])
        
        # Adding model 'WikiPageLog'
        db.create_table('wiki_wikipagelog', (
            ('content', models.TextField(null=False, blank=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('id', models.AutoField(primary_key=True)),
            ('wiki_page', models.ForeignKey(orm.WikiPage, null=False, blank=False)),
        ))
        db.send_create_signal('wiki', ['WikiPageLog'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'WikiPhoto'
        db.delete_table('wiki_wikiphoto')
        
        # Deleting model 'WikiFile'
        db.delete_table('wiki_wikifile')
        
        # Deleting model 'WikiPage'
        db.delete_table('wiki_wikipage')
        
        # Deleting model 'WikiPageLog'
        db.delete_table('wiki_wikipagelog')
        
    
    
    models = {
        'wiki.wikiphoto': {
            'Meta': {'ordering': "['-created']"},
            'caption': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {'blank': 'False'}),
            'title': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('models.ForeignKey', ['WikiPage'], {'null': 'False', 'blank': 'False'})
        },
        'wiki.wikifile': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('models.FileField', [], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('models.ForeignKey', ['WikiPage'], {'null': 'False', 'blank': 'False'})
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
            'wiki_page': ('models.ForeignKey', ['WikiPage'], {'null': 'False', 'blank': 'False'})
        }
    }
    
    complete_apps = ['wiki']
