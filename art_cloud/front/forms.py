from django import forms
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from models import *

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('display_name', 'bio', 'url')

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email',)
