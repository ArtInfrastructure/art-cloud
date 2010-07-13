# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import os.path
import urllib
import datetime, calendar
import re
import feedparser
import unicodedata
import traceback
import logging
import pprint

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from art_cloud.abstract_models import ThumbnailedModel
from templatetags.wikitags import wiki

class WikiPageManager(models.Manager):
	def get_or_create(self, name):
		try: return WikiPage.objects.get(name=name)
		except: return WikiPage(name=name)

class WikiPage(models.Model):
	"""A named chunk of markdown formatted text."""
	name = models.CharField(max_length=255, unique=True, blank=False, null=False)
	content = models.TextField(blank=False, null=False)
	rendered = models.TextField(blank=True, null=True)
	public = models.BooleanField(default=True)
	objects = WikiPageManager()
	@models.permalink
	def get_absolute_url(self):
		if self.name == "SplashPage": return ('wiki.views.index', [], {})
		return ('wiki.views.wiki', [], { 'name':self.name })
	@models.permalink
	def get_edit_url(self):
		return ('wiki.views.wiki_edit', [], { 'name':self.name })
	def __unicode__(self):
		return self.name
	def save(self, *args, **kwargs):
		"""When saving the content, render via markdown and save to self.rendered"""
		self.rendered = wiki(self.content)
		super(WikiPage, self).save(*args, **kwargs)
		WikiPageLog.objects.create(wiki_page=self, content=self.content)
	class Meta:
		ordering = ('name',)

class WikiPageLog(models.Model):
	"""A historical version of a WikiPage."""
	wiki_page = models.ForeignKey(WikiPage, blank=False, null=False)
	content = models.TextField(blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True)
	@models.permalink
	def get_absolute_url(self):
		return ('wiki.views.wiki_page_log', [], { 'name':self.wiki_page.name, 'id':self.id })
	def __unicode__(self):
		return '%s: %s' % (self.wiki_page.name, self.created)
	class Meta:
		ordering = ('-created',)

class WikiConstant(models.Model):
	"""A piece of wikitext which can be included (but not wiki rendered) in multiple wiki pages
	The syntax is \%constant_name\%
	"""
	name = models.CharField(max_length=512, null=False, blank=False)
	constant = models.TextField(blank=False, null=False)
	def __unicode__(self):
		return self.name

class WikiFile(models.Model):
	"""A non-image file associated with a WikiPage."""
	file = models.FileField(upload_to='wiki_file', blank=False, null=False)
	wiki_page = models.ForeignKey(WikiPage, blank=False, null=False)
	title = models.CharField(max_length=1024, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	def display_name(self):
		if self.title: return self.title
		return os.path.basename(self.file.name)
	@models.permalink
	def get_absolute_url(self):
		return ('wiki.views.file', (), { 'name':self.wiki_page.name, 'id':self.id })
	class Meta:
		ordering = ['-created']
	def __unicode__(self):
		return str(self.file)

class WikiPhoto(ThumbnailedModel):
	"""An image and metadata associated with a WikiPage."""
	image = models.ImageField(upload_to='wiki_photo', blank=False)
	wiki_page = models.ForeignKey(WikiPage, blank=False, null=False)
	title = models.CharField(max_length=1024, null=True, blank=True)
	caption = models.CharField(max_length=1024, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	def display_name(self):
		if self.title: return self.title
		return os.path.basename(self.image.name)
	@models.permalink
	def get_absolute_url(self):
		return ('wiki.views.photo', (), { 'name':self.wiki_page.name, 'id':self.id })
	class Meta:
		ordering = ['-created']
	def __unicode__(self):
		return str(self.image)
