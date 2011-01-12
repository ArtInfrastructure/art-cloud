# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import HelpText

class StyledAdmin(admin.ModelAdmin):
	"""A common base admin class with shared media information."""
	save_on_top=True
	class Media:
		css = { "all": ('art_cloud/admin.css', )}
		

class HelpTextAdmin(StyledAdmin):
	pass
admin.site.register(HelpText, HelpTextAdmin)