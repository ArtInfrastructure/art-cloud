# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import os.path
import Image
import urllib
import datetime, calendar
import random
import time
import re
import feedparser
import unicodedata
import traceback
import logging
import pprint

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.utils.encoding import force_unicode, smart_unicode
from django.db.models import Q
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.localflavor.us.forms import phone_digits_re

from art_cloud.abstract_models import ThumbnailedModel
from front.models import Installation

# Needed audio clips: splash audio, generic rotating artwork intro, art program intro, permanent pieces info

# Possible future uses:
# Notify art tech of problem
# Record a feedback clip, tell artist

class PhoneManager(models.Manager):
	def get_by_number(self, number):
		try:
			return self.get(phone_number=number)
		except:
			pass
	 	number = re.sub('(\(|\)|\s+)', '', smart_unicode(number))
		matches = phone_digits_re.search(number)
		if not matches: return None
		formatted_phone_number = '%s-%s-%s' % (matches.group(1), matches.group(2), matches.group(3))
		try:
			return self.get(phone_number=formatted_phone_number)
		except:
			return None
		
class Phone(models.Model):
	phone_number = PhoneNumberField(blank=False, null=False, unique=True)
	blocked = models.BooleanField(blank=False, null=False, default=False)
	objects = PhoneManager()
	def __unicode__(self):
	 	number = re.sub('(\(|\)|\s+)', '', self.phone_number)
		matches = phone_digits_re.search(number)
		if not matches: return self.phone_number
		return '(%s) %s-%s' % (matches.group(1), matches.group(2), matches.group(3))

class PhoneCall(models.Model):
	phone = models.ForeignKey(Phone, null=False, blank=False)
	guid = models.CharField(max_length=64, blank=False, null=False, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	completed = models.DateTimeField(blank=True, null=True)

class AudioClipManager(models.Manager):
	def default_landing_clip(self):
		if self.filter(landing_clip=True).count() == 0: return None
		return self.filter(landing_clip=True)[0]

class AudioClip(models.Model):
	name = models.CharField(max_length=1024, blank=False, null=False)
	audio = models.FileField(upload_to='phonon_audio_clip', blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True)
	landing_clip = models.BooleanField(blank=False, null=False, default=False)

	objects = AudioClipManager()
	def save(self, *args, **kwargs):
		super(AudioClip, self).save(*args, **kwargs)
		if self.landing_clip == True: # set all the other landing clips to not be landing clips
			for old_landing_clip in AudioClip.objects.filter(landing_clip=True):
				if old_landing_clip.id == self.id: continue
				old_landing_clip.landing_clip = False
				old_landing_clip.save()
	def __unicode__(self):
		return self.name

class InformationNode(models.Model):
	"""Information which is available via call or SMS"""
	name = models.CharField(max_length=1024, blank=False, null=False)
	code = models.PositiveIntegerField(unique=True, blank=False, null=False); # The numeric code which a caller punches in to identify an installation
	introduction = models.ForeignKey(AudioClip, blank=False, null=False)
	installation = models.ForeignKey(Installation, blank=True, null=True) # Artwork which is associated with this node
	class Meta:
		ordering = ['name']
	def __unicode__(self):
		return self.name
