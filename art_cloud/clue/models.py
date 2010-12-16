# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import os.path
import urllib
import datetime, calendar
import random
import time
import re
import unicodedata
import traceback
import logging
import pprint
import string

from django.template.loader import render_to_string
from django.utils.html import strip_tags,  linebreaks, urlize
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.utils.encoding import force_unicode
from django.db.models import Q

from django.contrib.markup.templatetags.markup import markdown

class HelpText(models.Model):
	"""A named snippet of markdown text for inclusion in displayed help."""
	name = models.CharField(max_length=256, blank=False, null=False, unique=True)
	content = models.TextField(blank=False, null=False)
	rendered = models.TextField(blank=True, null=True, editable=False)

	def __unicode__(self):
		return '%s' % self.name
	class Meta:
		ordering = ('name',)

	def save(self, *args, **kwargs):
		"""When saving the content, render via markdown and save to self.rendered"""
		self.rendered = markdown(self.content)
		super(HelpText, self).save(*args, **kwargs)
