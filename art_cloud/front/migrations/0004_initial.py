
from south.db import db
from django.db import models
from art_cloud.front.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Heartbeat'
        db.create_table('front_heartbeat', (
            ('id', orm['front.Heartbeat:id']),
            ('installation', orm['front.Heartbeat:installation']),
            ('info', orm['front.Heartbeat:info']),
            ('created', orm['front.Heartbeat:created']),
        ))
        db.send_create_signal('front', ['Heartbeat'])
        
        # Adding model 'InstallationSite'
        db.create_table('front_installationsite', (
            ('id', orm['front.InstallationSite:id']),
            ('name', orm['front.InstallationSite:name']),
            ('location', orm['front.InstallationSite:location']),
            ('notes', orm['front.InstallationSite:notes']),
        ))
        db.send_create_signal('front', ['InstallationSite'])
        
        # Adding model 'Equipment'
        db.create_table('front_equipment', (
            ('id', orm['front.Equipment:id']),
            ('name', orm['front.Equipment:name']),
            ('equipment_type', orm['front.Equipment:equipment_type']),
            ('notes', orm['front.Equipment:notes']),
        ))
        db.send_create_signal('front', ['Equipment'])
        
        # Adding model 'EquipmentType'
        db.create_table('front_equipmenttype', (
            ('id', orm['front.EquipmentType:id']),
            ('name', orm['front.EquipmentType:name']),
            ('provider', orm['front.EquipmentType:provider']),
            ('url', orm['front.EquipmentType:url']),
            ('notes', orm['front.EquipmentType:notes']),
        ))
        db.send_create_signal('front', ['EquipmentType'])
        
        # Adding model 'Photo'
        db.create_table('front_photo', (
            ('id', orm['front.Photo:id']),
            ('image', orm['front.Photo:image']),
            ('title', orm['front.Photo:title']),
            ('caption', orm['front.Photo:caption']),
            ('description', orm['front.Photo:description']),
            ('created', orm['front.Photo:created']),
        ))
        db.send_create_signal('front', ['Photo'])
        
        # Adding model 'Installation'
        db.create_table('front_installation', (
            ('id', orm['front.Installation:id']),
            ('name', orm['front.Installation:name']),
            ('slug', orm['front.Installation:slug']),
            ('site', orm['front.Installation:site']),
            ('opened', orm['front.Installation:opened']),
            ('closed', orm['front.Installation:closed']),
            ('notes', orm['front.Installation:notes']),
            ('wiki_name', orm['front.Installation:wiki_name']),
        ))
        db.send_create_signal('front', ['Installation'])
        
        # Adding model 'ArtistGroup'
        db.create_table('front_artistgroup', (
            ('id', orm['front.ArtistGroup:id']),
            ('name', orm['front.ArtistGroup:name']),
            ('url', orm['front.ArtistGroup:url']),
        ))
        db.send_create_signal('front', ['ArtistGroup'])
        
        # Adding model 'UserProfile'
        db.create_table('front_userprofile', (
            ('id', orm['front.UserProfile:id']),
            ('user', orm['front.UserProfile:user']),
            ('display_name', orm['front.UserProfile:display_name']),
            ('bio', orm['front.UserProfile:bio']),
            ('url', orm['front.UserProfile:url']),
            ('phone_number', orm['front.UserProfile:phone_number']),
        ))
        db.send_create_signal('front', ['UserProfile'])
        
        # Adding ManyToManyField 'Installation.artists'
        db.create_table('front_installation_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installation', models.ForeignKey(orm.Installation, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'ArtistGroup.artists'
        db.create_table('front_artistgroup_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artistgroup', models.ForeignKey(orm.ArtistGroup, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'Installation.photos'
        db.create_table('front_installation_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installation', models.ForeignKey(orm.Installation, null=False)),
            ('photo', models.ForeignKey(orm.Photo, null=False))
        ))
        
        # Adding ManyToManyField 'Equipment.photos'
        db.create_table('front_equipment_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm.Equipment, null=False)),
            ('photo', models.ForeignKey(orm.Photo, null=False))
        ))
        
        # Adding ManyToManyField 'InstallationSite.photos'
        db.create_table('front_installationsite_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installationsite', models.ForeignKey(orm.InstallationSite, null=False)),
            ('photo', models.ForeignKey(orm.Photo, null=False))
        ))
        
        # Adding ManyToManyField 'InstallationSite.equipment'
        db.create_table('front_installationsite_equipment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installationsite', models.ForeignKey(orm.InstallationSite, null=False)),
            ('equipment', models.ForeignKey(orm.Equipment, null=False))
        ))
        
        # Adding ManyToManyField 'Installation.groups'
        db.create_table('front_installation_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installation', models.ForeignKey(orm.Installation, null=False)),
            ('artistgroup', models.ForeignKey(orm.ArtistGroup, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Heartbeat'
        db.delete_table('front_heartbeat')
        
        # Deleting model 'InstallationSite'
        db.delete_table('front_installationsite')
        
        # Deleting model 'Equipment'
        db.delete_table('front_equipment')
        
        # Deleting model 'EquipmentType'
        db.delete_table('front_equipmenttype')
        
        # Deleting model 'Photo'
        db.delete_table('front_photo')
        
        # Deleting model 'Installation'
        db.delete_table('front_installation')
        
        # Deleting model 'ArtistGroup'
        db.delete_table('front_artistgroup')
        
        # Deleting model 'UserProfile'
        db.delete_table('front_userprofile')
        
        # Dropping ManyToManyField 'Installation.artists'
        db.delete_table('front_installation_artists')
        
        # Dropping ManyToManyField 'ArtistGroup.artists'
        db.delete_table('front_artistgroup_artists')
        
        # Dropping ManyToManyField 'Installation.photos'
        db.delete_table('front_installation_photos')
        
        # Dropping ManyToManyField 'Equipment.photos'
        db.delete_table('front_equipment_photos')
        
        # Dropping ManyToManyField 'InstallationSite.photos'
        db.delete_table('front_installationsite_photos')
        
        # Dropping ManyToManyField 'InstallationSite.equipment'
        db.delete_table('front_installationsite_equipment')
        
        # Dropping ManyToManyField 'Installation.groups'
        db.delete_table('front_installation_groups')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'front.artistgroup': {
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'front.equipment': {
            'equipment_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['front.EquipmentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['front.Photo']", 'null': 'True', 'blank': 'True'})
        },
        'front.equipmenttype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'front.heartbeat': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'installation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['front.Installation']"})
        },
        'front.installation': {
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['front.ArtistGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['front.Photo']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['front.InstallationSite']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'wiki_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'front.installationsite': {
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['front.Equipment']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['front.Photo']", 'null': 'True', 'blank': 'True'})
        },
        'front.photo': {
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'front.userprofile': {
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['front']
