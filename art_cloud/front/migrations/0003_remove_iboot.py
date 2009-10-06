
from south.db import db
from django.db import models
from art_cloud.front.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Dropping ManyToManyField 'InstallationSite.iboots'
        db.delete_table('front_installationsite_iboots')
        
    
    
    def backwards(self, orm):
        
        # Adding ManyToManyField 'InstallationSite.iboots'
        db.create_table('front_installationsite_iboots', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installationsite', models.ForeignKey(orm.InstallationSite, null=False)),
            ('ibootdevice', models.ForeignKey(orm['iboot.ibootdevice'], null=False))
        ))
        
    
    
    models = {
        'front.installationsite': {
            'Meta': {'ordering': "['name']"},
            'equipment': ('models.ManyToManyField', ["orm['front.Equipment']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('models.ManyToManyField', ["orm['front.Photo']"], {'null': 'True', 'blank': 'True'})
        },
        'front.equipment': {
            'Meta': {'ordering': "['name']"},
            'equipment_type': ('models.ForeignKey', ["orm['front.EquipmentType']"], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('models.ManyToManyField', ["orm['front.Photo']"], {'null': 'True', 'blank': 'True'})
        },
        'front.heartbeat': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'info': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'installation': ('models.ForeignKey', ["orm['front.Installation']"], {'null': 'False', 'blank': 'False'})
        },
        'front.equipmenttype': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'provider': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('models.URLField', [], {'max_length': '1024', 'blank': 'True', 'null': 'True', 'verify_exists': 'False'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'front.photo': {
            'Meta': {'ordering': "['-created']"},
            'caption': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {'blank': 'False'}),
            'title': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'front.installation': {
            'Meta': {'ordering': "['name']"},
            'artists': ('models.ManyToManyField', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'closed': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('models.ManyToManyField', ["orm['front.ArtistGroup']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opened': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('models.ManyToManyField', ["orm['front.Photo']"], {'null': 'True', 'blank': 'True'}),
            'site': ('models.ForeignKey', ["orm['front.InstallationSite']"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'null': 'True', 'blank': 'True'}),
            'wiki_name': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'front.artistgroup': {
            'Meta': {'ordering': "['name']"},
            'artists': ('models.ManyToManyField', ["orm['auth.User']"], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'url': ('models.URLField', [], {'max_length': '1024', 'blank': 'True', 'null': 'True', 'verify_exists': 'False'})
        },
        'iboot.ibootdevice': {
            'Meta': {'ordering': "['name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'front.userprofile': {
            'Meta': {'ordering': "['user__username']"},
            'bio': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('models.CharField', [], {'max_length': '1024'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('models.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('models.URLField', [], {'blank': 'True', 'max_length': '300', 'null': 'True', 'verify_exists': 'False'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'unique': 'True'})
        }
    }
    
    complete_apps = ['front']
