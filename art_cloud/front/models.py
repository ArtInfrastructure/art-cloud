# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
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
from django.utils.encoding import force_unicode

from art_cloud.abstract_models import ThumbnailedModel
from tagging.models import Tag

class ArtistGroup(models.Model):
	"""A group of artists who collectively create installations, perhaps also with individual artists."""
	name = models.CharField(max_length=1024, blank=False, null=False)
	artists = models.ManyToManyField(User, blank=False, null=False)
	url = models.URLField(verify_exists=False, blank=True, null=True, max_length=1024)
	class Meta:
		ordering = ['name']
	@models.permalink
	def get_absolute_url(self):
		return ('art_cloud.front.views.artist_group_detail', (), { 'id':self.id })
	def __unicode__(self):
		return self.name

class Photo(ThumbnailedModel):
	image = models.ImageField(upload_to='photo', blank=False)
	title = models.CharField(max_length=1024, null=False, blank=False)
	caption = models.CharField(max_length=1024, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	@models.permalink
	def get_absolute_url(self):
		return ('art_cloud.front.views.photo_detail', (), { 'id':self.id })
	class Meta:
		ordering = ['-created']
	def __unicode__(self):
		return str(self.image)

class EquipmentType(models.Model):
	name = models.CharField(max_length=1024, null=False, blank=False)
	provider = models.TextField(null=True, blank=True)
	url = models.URLField(verify_exists=False, blank=True, null=True, max_length=1024)
	notes = models.TextField(blank=True, null=True)
	@models.permalink
	def get_absolute_url(self):
		return ('art_cloud.front.views.equipment_type_detail', (), { 'id':self.id })
	class Meta:
		ordering = ['name']
	def __unicode__(self):
		return self.name

class Equipment(models.Model):
	name = models.CharField(max_length=1024, null=False, blank=False)
	equipment_type = models.ForeignKey(EquipmentType, blank=False, null=False)
	photos = models.ManyToManyField(Photo, null=True, blank=True)
	notes = models.TextField(blank=True, null=True)
	@models.permalink
	def get_absolute_url(self):
		return ('art_cloud.front.views.equipment_detail', (), { 'id':self.id })
	class Meta:
		verbose_name_plural = 'equipment'
		ordering = ['name']
	def __unicode__(self):
		return "%s:%s" % (self.equipment_type.name, self.name)

class InstallationSite(models.Model):
	name = models.CharField(max_length=1024, null=False, blank=False)
	location = models.CharField(max_length=1024, null=True, blank=True)
	notes = models.TextField(blank=True, null=True)
	photos = models.ManyToManyField(Photo, null=True, blank=True)
	equipment = models.ManyToManyField(Equipment, null=True, blank=True)
	@models.permalink
	def get_absolute_url(self):
		return ('art_cloud.front.views.installation_site_detail', (), { 'id':self.id })
	class Meta:
		verbose_name =  'location'
		verbose_name_plural = 'locations'
		ordering = ['name']
	def __unicode__(self):
		return self.name

class InstallationManager(models.Manager):
	def all_open(self):
		return self.filter(closed=None) | self.filter(closed__gt=datetime.datetime.now())

class Installation(models.Model):
	name = models.CharField(max_length=1024, null=False, blank=False)
	slug = models.SlugField(blank=True, null=True)
	groups = models.ManyToManyField(ArtistGroup, null=True, blank=True)
	artists = models.ManyToManyField(User, null=True, blank=True)
	site = models.ForeignKey(InstallationSite, null=True, blank=True)
	opened = models.DateTimeField(null=True, blank=True)
	closed = models.DateTimeField(null=True, blank=True)
	notes = models.TextField(blank=True, null=True)
	photos = models.ManyToManyField(Photo, null=True, blank=True)
	wiki_name = models.CharField(max_length=255, blank=True, null=True)
	objects = InstallationManager()

	def _get_tags(self):
		return Tag.objects.get_for_object(self)
	def _set_tags(self, tag_list):
		Tag.objects.update_tags(self, tag_list)
	tags = property(_get_tags, _set_tags)
	def _get_tag_names(self):
		return " ".join([tag.name for tag in self.tags])
	tag_names = property(_get_tag_names, _set_tags)

	def is_opened(self):
		if self.is_closed(): return False
		if self.opened == None: return False
		return self.opened < datetime.datetime.now()
	is_opened.boolean = True

	def is_closed(self):
		if self.closed == None: return False
		return self.closed < datetime.datetime.now()
	
	@models.permalink
	def get_absolute_url(self):
		if self.slug:
			return ('art_cloud.front.views.installation_detail_slug', (), { 'slug':self.slug })
		else:
			return ('art_cloud.front.views.installation_detail', (), { 'id':self.id })
	class Meta:
		verbose_name =  'artwork'
		verbose_name_plural = 'works of art'
		ordering = ['name']
	def __unicode__(self):
		return self.name

class HeartbeatManager(models.Manager):
	def delete_old_heartbeats(self):
		deadline = datetime.datetime.now() - datetime.timedelta(days=2)
		for heartbeat in self.filter(created__lt=deadline):
			heartbeat.delete()

class Heartbeat(models.Model):
	installation = models.ForeignKey(Installation, null=False, blank=False)
	info = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	
	objects = HeartbeatManager()
	
	def trimmed_info(self):
		if self.info: 
			if len(self.info) > 60:
				return self.info[:60] + '...'
			return self.info
		return None
	def timed_out(self):
		return self.created + datetime.timedelta(seconds=settings.HEARTBEAT_TIMEOUT) < datetime.datetime.now() 
	class Meta:
		ordering = ['-created']
	def __unicode__(self):
		return "%s: %s" % (self.installation, self.created)

class UserProfileManager(models.Manager):
	def notify_art_technician(self, subject, message_text):
		message = render_to_string('front/email/tech_notification.txt', { 'message': message_text })
		for user in User.objects.filter(groups__name="technicians"):
			user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

class UserProfile(models.Model):
	"""Extends the django.contrib.auth User model"""
	user = models.ForeignKey(User, unique=True)
	display_name = models.CharField(max_length=1024)
	bio = models.TextField(null=True, blank=True)
	url = models.URLField(verify_exists=False, null=True, blank=True, max_length=300)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	objects = UserProfileManager()
	
	@models.permalink
	def get_absolute_url(self):
		return ('art_cloud.front.views.profile_detail', (), { 'username':urllib.quote(self.user.username) })
	def is_artist(self):
		for group in self.user.groups.all():
			if group.name == 'artists': return True
		return False
	def __unicode__(self):
		return self.user.username
	class Meta:
		verbose_name = 'artist profile'
		verbose_name_plural = 'artist profiles'
		ordering = ['user__username']

def user_post_save(sender, instance, signal, *args, **kwargs):
	"""Ensures that a profile is created for each user when saved."""
	profile, new = UserProfile.objects.get_or_create(user=instance)
	if new:
		profile.display_name = instance.username
		profile.save()
signals.post_save.connect(user_post_save, sender=User)
