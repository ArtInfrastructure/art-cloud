
from south.db import db
from django.db import models
from art_cloud.front.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Heartbeat'
        db.create_table('front_heartbeat', (
            ('info', models.TextField(null=True, blank=True)),
            ('installation', models.ForeignKey(orm.Installation, null=False, blank=False)),
            ('id', models.AutoField(primary_key=True)),
            ('created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('front', ['Heartbeat'])
        
        # Adding model 'InstallationSite'
        db.create_table('front_installationsite', (
            ('notes', models.TextField(null=True, blank=True)),
            ('location', models.CharField(max_length=1024, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['InstallationSite'])
        
        # Adding model 'Equipment'
        db.create_table('front_equipment', (
            ('equipment_type', models.ForeignKey(orm.EquipmentType, null=False, blank=False)),
            ('notes', models.TextField(null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['Equipment'])
        
        # Adding model 'EquipmentType'
        db.create_table('front_equipmenttype', (
            ('url', models.URLField(max_length=1024, blank=True, null=True, verify_exists=False)),
            ('notes', models.TextField(null=True, blank=True)),
            ('provider', models.TextField(null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['EquipmentType'])
        
        # Adding model 'Photo'
        db.create_table('front_photo', (
            ('description', models.TextField(null=True, blank=True)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('image', models.ImageField(blank=False)),
            ('title', models.CharField(max_length=1024, null=True, blank=True)),
            ('caption', models.CharField(max_length=1024, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('front', ['Photo'])
        
        # Adding model 'Installation'
        db.create_table('front_installation', (
            ('opened', models.DateTimeField(null=True, blank=True)),
            ('notes', models.TextField(null=True, blank=True)),
            ('site', models.ForeignKey(orm.InstallationSite, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('closed', models.DateTimeField(null=True, blank=True)),
            ('wiki_name', models.CharField(max_length=255, null=True, blank=True)),
            ('slug', models.SlugField(null=True, blank=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['Installation'])
        
        # Adding model 'ArtistGroup'
        db.create_table('front_artistgroup', (
            ('url', models.URLField(max_length=1024, blank=True, null=True, verify_exists=False)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=1024, null=False, blank=False)),
        ))
        db.send_create_signal('front', ['ArtistGroup'])
        
        # Adding model 'UserProfile'
        db.create_table('front_userprofile', (
            ('phone_number', models.CharField(max_length=20, null=True, blank=True)),
            ('bio', models.TextField(null=True, blank=True)),
            ('display_name', models.CharField(max_length=1024)),
            ('url', models.URLField(blank=True, max_length=300, null=True, verify_exists=False)),
            ('user', models.ForeignKey(orm['auth.User'], unique=True)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('front', ['UserProfile'])
        
        # Adding ManyToManyField 'Installation.artists'
        db.create_table('front_installation_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installation', models.ForeignKey(Installation, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
        # Adding ManyToManyField 'ArtistGroup.artists'
        db.create_table('front_artistgroup_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artistgroup', models.ForeignKey(ArtistGroup, null=False)),
            ('user', models.ForeignKey(User, null=False))
        ))
        
        # Adding ManyToManyField 'Installation.photos'
        db.create_table('front_installation_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installation', models.ForeignKey(Installation, null=False)),
            ('photo', models.ForeignKey(Photo, null=False))
        ))
        
        # Adding ManyToManyField 'Equipment.photos'
        db.create_table('front_equipment_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(Equipment, null=False)),
            ('photo', models.ForeignKey(Photo, null=False))
        ))
        
        # Adding ManyToManyField 'InstallationSite.photos'
        db.create_table('front_installationsite_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installationsite', models.ForeignKey(InstallationSite, null=False)),
            ('photo', models.ForeignKey(Photo, null=False))
        ))
        
        # Adding ManyToManyField 'InstallationSite.equipment'
        db.create_table('front_installationsite_equipment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installationsite', models.ForeignKey(InstallationSite, null=False)),
            ('equipment', models.ForeignKey(Equipment, null=False))
        ))
        
        # Adding ManyToManyField 'Installation.groups'
        db.create_table('front_installation_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installation', models.ForeignKey(Installation, null=False)),
            ('artistgroup', models.ForeignKey(ArtistGroup, null=False))
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
        'front.installationsite': {
            'Meta': {'ordering': "['name']"},
            'equipment': ('models.ManyToManyField', ['Equipment'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('models.ManyToManyField', ['Photo'], {'null': 'True', 'blank': 'True'})
        },
        'front.equipment': {
            'Meta': {'ordering': "['name']"},
            'equipment_type': ('models.ForeignKey', ['EquipmentType'], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('models.ManyToManyField', ['Photo'], {'null': 'True', 'blank': 'True'})
        },
        'front.equipmenttype': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'provider': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('models.URLField', [], {'max_length': '1024', 'blank': 'True', 'null': 'True', 'verify_exists': 'False'})
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
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'front.heartbeat': {
            'Meta': {'ordering': "['-created']"},
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'info': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'installation': ('models.ForeignKey', ['Installation'], {'null': 'False', 'blank': 'False'})
        },
        'front.installation': {
            'Meta': {'ordering': "['name']"},
            'artists': ('models.ManyToManyField', ['User'], {'null': 'True', 'blank': 'True'}),
            'closed': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('models.ManyToManyField', ['ArtistGroup'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'notes': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opened': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('models.ManyToManyField', ['Photo'], {'null': 'True', 'blank': 'True'}),
            'site': ('models.ForeignKey', ['InstallationSite'], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'null': 'True', 'blank': 'True'}),
            'wiki_name': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'front.artistgroup': {
            'Meta': {'ordering': "['name']"},
            'artists': ('models.ManyToManyField', ['User'], {'null': 'False', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '1024', 'null': 'False', 'blank': 'False'}),
            'url': ('models.URLField', [], {'max_length': '1024', 'blank': 'True', 'null': 'True', 'verify_exists': 'False'})
        },
        'front.userprofile': {
            'Meta': {'ordering': "['user__username']"},
            'bio': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('models.CharField', [], {'max_length': '1024'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('models.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('models.URLField', [], {'blank': 'True', 'max_length': '300', 'null': 'True', 'verify_exists': 'False'}),
            'user': ('models.ForeignKey', ['User'], {'unique': 'True'})
        }
    }
    
    complete_apps = ['front']
