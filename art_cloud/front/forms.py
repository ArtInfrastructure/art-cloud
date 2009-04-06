# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django import forms
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from models import *

class SearchForm(forms.Form):
	terms = forms.CharField(required=True)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('display_name', 'bio', 'url', 'phone_number')

class InstallationNotesForm(forms.Form):
	notes = forms.CharField(required=False, widget=forms.Textarea())

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email',)

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo

class TagsForm(forms.Form):
	tags = forms.CharField(required=False)
