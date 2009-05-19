# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import *

class StyledModelAdmin(admin.ModelAdmin):
	"""A common base admin class with shared media information."""
	save_on_top=True
	class Media:
		css = { "all": ('art_cloud/admin.css', )}

class HeartbeatAdmin(StyledModelAdmin):
	list_display = ('installation', 'created', 'trimmed_info')
	date_hierarchy = 'created'
	search_fields = ('installation__name', )
admin.site.register(Heartbeat, HeartbeatAdmin)	

class ArtistGroupAdmin(StyledModelAdmin):
	filter_horizontal = ('artists',)
admin.site.register(ArtistGroup, ArtistGroupAdmin)	

class UserProfileAdmin(StyledModelAdmin):
	list_display = ('user', 'display_name')
admin.site.register(UserProfile, UserProfileAdmin)	

class PhotoAdmin(StyledModelAdmin):
	list_display = ('display_name', 'image', 'thumb')
	search_fields = ('title', 'image')
admin.site.register(Photo, PhotoAdmin)	

class EquipmentTypeAdmin(StyledModelAdmin):
	pass
admin.site.register(EquipmentType, EquipmentTypeAdmin)

class EquipmentAdmin(StyledModelAdmin):
	filter_horizontal = ('photos',)
admin.site.register(Equipment, EquipmentAdmin)

class InstallationSiteAdmin(StyledModelAdmin):
	filter_horizontal = ('photos', 'equipment', 'iboots')
admin.site.register(InstallationSite, InstallationSiteAdmin)

class InstallationAdmin(StyledModelAdmin):
	list_display = ('name', 'site', 'is_opened')
	filter_horizontal = ('artists', 'groups', 'photos')
admin.site.register(Installation, InstallationAdmin)
