from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import *

class StyledModelAdmin(admin.ModelAdmin):
	save_on_top=True
	class Media:
		css = { "all": ('art_cloud/admin.css', )}

class UserProfileAdmin(StyledModelAdmin):
	pass
admin.site.register(UserProfile, UserProfileAdmin)	

class PhotoAdmin(StyledModelAdmin):
	pass
admin.site.register(Photo, PhotoAdmin)	

class EquipmentTypeAdmin(StyledModelAdmin):
	pass
admin.site.register(EquipmentType, EquipmentTypeAdmin)

class EquipmentAdmin(StyledModelAdmin):
	filter_horizontal = ('photos',)
	pass
admin.site.register(Equipment, EquipmentAdmin)

class InstallationSiteAdmin(StyledModelAdmin):
	filter_horizontal = ('photos', 'equipment')
	pass
admin.site.register(InstallationSite, InstallationSiteAdmin)

class InstallationAdmin(StyledModelAdmin):
	filter_horizontal = ('artists', 'photos')
	pass
admin.site.register(Installation, InstallationAdmin)
