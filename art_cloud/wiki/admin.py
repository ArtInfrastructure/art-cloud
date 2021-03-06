# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import *

class StyledModelAdmin(admin.ModelAdmin):
	save_on_top=True
	class Media:
		css = { "all": ('art_cloud/admin.css', )}

class WikiConstantAdmin(StyledModelAdmin):
	search_fields = ('name','constant')
	list_display = ('name', 'constant')
admin.site.register(WikiConstant, WikiConstantAdmin)	

class WikiPageAdmin(StyledModelAdmin):
	search_fields = ('name','content')
	list_display = ('name', 'public')
	list_editable = ('public',)
	#fields = ('name', 'content', 'public')
admin.site.register(WikiPage, WikiPageAdmin)	

class WikiFileAdmin(StyledModelAdmin):
	search_fields = ('file','title','description')
	list_display = ('display_name', 'description', 'wiki_page')
admin.site.register(WikiFile, WikiFileAdmin)	

class WikiPhotoAdmin(StyledModelAdmin):
	search_fields = ('image','title','description')
	list_display = ('display_name', 'description', 'wiki_page')
admin.site.register(WikiPhoto, WikiPhotoAdmin)	

class WikiPageLogAdmin(StyledModelAdmin):
	search_fields = ('wiki_page__name','content')
admin.site.register(WikiPageLog, WikiPageLogAdmin)	
