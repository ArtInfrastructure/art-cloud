
from south.db import db
from django.db import models
from art_cloud.datonomy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'NamedDate'
        db.create_table('datonomy_nameddate', (
            ('date', models.DateField(null=False, blank=False)),
            ('object_id', models.PositiveIntegerField()),
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'])),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('datonomy', ['NamedDate'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'NamedDate'
        db.delete_table('datonomy_nameddate')
        
    
    
    models = {
        'datonomy.nameddate': {
            'Meta': {'ordering': "['date']"},
            'content_type': ('models.ForeignKey', ['ContentType'], {}),
            'date': ('models.DateField', [], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'object_id': ('models.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['datonomy']
