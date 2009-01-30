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

from django.utils.html import strip_tags
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.utils.encoding import force_unicode

class Photo(models.Model):
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
		ordering = ['name']
	def __unicode__(self):
		return self.name

class InstallationManager(models.Manager):
	def all_open(self):
		return self.filter(closed=None) | self.filter(closed__gt=datetime.datetime.now())

class Installation(models.Model):
	name = models.CharField(max_length=1024, null=False, blank=False)
	artists = models.ManyToManyField(User, null=False, blank=False)
	site = models.ForeignKey(InstallationSite, null=True, blank=True)
	opened = models.DateTimeField(null=True, blank=True)
	closed = models.DateTimeField(null=True, blank=True)
	notes = models.TextField(blank=True, null=True)
	photos = models.ManyToManyField(Photo, null=True, blank=True)
	
	objects = InstallationManager()

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
		return ('art_cloud.front.views.installation_detail', (), { 'id':self.id })
	class Meta:
		ordering = ['name']
	def __unicode__(self):
		return self.name

class Heartbeat(models.Model):
	installation = models.ForeignKey(Installation, null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True)
	def timed_out(self):
		return self.created + datetime.timedelta(seconds=settings.HEARTBEAT_TIMEOUT) < datetime.datetime.now() 
	class Meta:
		ordering = ['-created']
	def __unicode__(self):
		return "%s: %s" % (self.installation, self.created)
class UserProfile(models.Model):
	"""Extends the django.contrib.auth User model"""
	user = models.ForeignKey(User, unique=True)
	display_name = models.CharField(max_length=1024)
	bio = models.TextField(null=True, blank=True)
	url = models.URLField(verify_exists=False, null=True, blank=True, max_length=300)
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
		ordering = ['user__username']

def user_post_save(sender, instance, signal, *args, **kwargs):
	"""Ensures that a profile is created for each user when saved."""
	profile, new = UserProfile.objects.get_or_create(user=instance)
	if new:
		profile.display_name = instance.username
		profile.save()
signals.post_save.connect(user_post_save, sender=User)
