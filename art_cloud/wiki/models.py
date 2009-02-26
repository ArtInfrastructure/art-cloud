# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
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

from templatetags.wikitags import wiki

class WikiPage(models.Model):
	name = models.CharField(max_length=255, unique=True, blank=False, null=False)
	content = models.TextField(blank=False, null=False)
	rendered = models.TextField(blank=True, null=True)
	@models.permalink
	def get_absolute_url(self):
		return ('wiki.views.wiki', [], { 'name':self.name })
	def __unicode__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.rendered = wiki(self.content)
		super(WikiPage, self).save(*args, **kwargs)
	class Meta:
		ordering = ('name',)
