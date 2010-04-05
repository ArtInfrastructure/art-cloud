
from south.db import db
from django.db import models
from art_cloud.wiki.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'WikiPage.public'
        db.add_column('wiki_wikipage', 'public', orm['wiki.wikipage:public'])
        
        # Changing field 'WikiPhoto.created'
        # (to signature: django.db.models.fields.DateTimeField(auto_now_add=True, blank=True))
        db.alter_column('wiki_wikiphoto', 'created', orm['wiki.wikiphoto:created'])
        
        # Changing field 'WikiPhoto.image'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100))
        db.alter_column('wiki_wikiphoto', 'image', orm['wiki.wikiphoto:image'])
        
        # Changing field 'WikiPhoto.wiki_page'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['wiki.WikiPage']))
        db.alter_column('wiki_wikiphoto', 'wiki_page_id', orm['wiki.wikiphoto:wiki_page'])
        
        # Changing field 'WikiFile.created'
        # (to signature: django.db.models.fields.DateTimeField(auto_now_add=True, blank=True))
        db.alter_column('wiki_wikifile', 'created', orm['wiki.wikifile:created'])
        
        # Changing field 'WikiFile.file'
        # (to signature: django.db.models.fields.files.FileField(max_length=100))
        db.alter_column('wiki_wikifile', 'file', orm['wiki.wikifile:file'])
        
        # Changing field 'WikiFile.wiki_page'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['wiki.WikiPage']))
        db.alter_column('wiki_wikifile', 'wiki_page_id', orm['wiki.wikifile:wiki_page'])
        
        # Changing field 'WikiConstant.constant'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column('wiki_wikiconstant', 'constant', orm['wiki.wikiconstant:constant'])
        
        # Changing field 'WikiConstant.name'
        # (to signature: django.db.models.fields.CharField(max_length=512))
        db.alter_column('wiki_wikiconstant', 'name', orm['wiki.wikiconstant:name'])
        
        # Changing field 'WikiPage.content'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column('wiki_wikipage', 'content', orm['wiki.wikipage:content'])
        
        # Changing field 'WikiPage.name'
        # (to signature: django.db.models.fields.CharField(unique=True, max_length=255))
        db.alter_column('wiki_wikipage', 'name', orm['wiki.wikipage:name'])
        
        # Changing field 'WikiPageLog.content'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column('wiki_wikipagelog', 'content', orm['wiki.wikipagelog:content'])
        
        # Changing field 'WikiPageLog.created'
        # (to signature: django.db.models.fields.DateTimeField(auto_now_add=True, blank=True))
        db.alter_column('wiki_wikipagelog', 'created', orm['wiki.wikipagelog:created'])
        
        # Changing field 'WikiPageLog.wiki_page'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['wiki.WikiPage']))
        db.alter_column('wiki_wikipagelog', 'wiki_page_id', orm['wiki.wikipagelog:wiki_page'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'WikiPage.public'
        db.delete_column('wiki_wikipage', 'public')
        
        # Changing field 'WikiPhoto.created'
        # (to signature: models.DateTimeField(auto_now_add=True))
        db.alter_column('wiki_wikiphoto', 'created', orm['wiki.wikiphoto:created'])
        
        # Changing field 'WikiPhoto.image'
        # (to signature: models.ImageField(blank=False))
        db.alter_column('wiki_wikiphoto', 'image', orm['wiki.wikiphoto:image'])
        
        # Changing field 'WikiPhoto.wiki_page'
        # (to signature: models.ForeignKey(orm['wiki.WikiPage'], null=False, blank=False))
        db.alter_column('wiki_wikiphoto', 'wiki_page_id', orm['wiki.wikiphoto:wiki_page'])
        
        # Changing field 'WikiFile.created'
        # (to signature: models.DateTimeField(auto_now_add=True))
        db.alter_column('wiki_wikifile', 'created', orm['wiki.wikifile:created'])
        
        # Changing field 'WikiFile.file'
        # (to signature: models.FileField(null=False, blank=False))
        db.alter_column('wiki_wikifile', 'file', orm['wiki.wikifile:file'])
        
        # Changing field 'WikiFile.wiki_page'
        # (to signature: models.ForeignKey(orm['wiki.WikiPage'], null=False, blank=False))
        db.alter_column('wiki_wikifile', 'wiki_page_id', orm['wiki.wikifile:wiki_page'])
        
        # Changing field 'WikiConstant.constant'
        # (to signature: models.TextField(null=False, blank=False))
        db.alter_column('wiki_wikiconstant', 'constant', orm['wiki.wikiconstant:constant'])
        
        # Changing field 'WikiConstant.name'
        # (to signature: models.CharField(max_length=512, null=False, blank=False))
        db.alter_column('wiki_wikiconstant', 'name', orm['wiki.wikiconstant:name'])
        
        # Changing field 'WikiPage.content'
        # (to signature: models.TextField(null=False, blank=False))
        db.alter_column('wiki_wikipage', 'content', orm['wiki.wikipage:content'])
        
        # Changing field 'WikiPage.name'
        # (to signature: models.CharField(max_length=255, unique=True, null=False, blank=False))
        db.alter_column('wiki_wikipage', 'name', orm['wiki.wikipage:name'])
        
        # Changing field 'WikiPageLog.content'
        # (to signature: models.TextField(null=False, blank=False))
        db.alter_column('wiki_wikipagelog', 'content', orm['wiki.wikipagelog:content'])
        
        # Changing field 'WikiPageLog.created'
        # (to signature: models.DateTimeField(auto_now_add=True))
        db.alter_column('wiki_wikipagelog', 'created', orm['wiki.wikipagelog:created'])
        
        # Changing field 'WikiPageLog.wiki_page'
        # (to signature: models.ForeignKey(orm['wiki.WikiPage'], null=False, blank=False))
        db.alter_column('wiki_wikipagelog', 'wiki_page_id', orm['wiki.wikipagelog:wiki_page'])
        
    
    
    models = {
        'wiki.wikiconstant': {
            'constant': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'wiki.wikifile': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.WikiPage']"})
        },
        'wiki.wikipage': {
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rendered': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'wiki.wikipagelog': {
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.WikiPage']"})
        },
        'wiki.wikiphoto': {
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.WikiPage']"})
        }
    }
    
    complete_apps = ['wiki']
