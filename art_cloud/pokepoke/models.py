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
import string

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
from django.db.models import Q

def create_secret():
	for i in range(0, 2000):
		secret = "".join(random.sample(string.letters+string.digits, 62))
		if AlertPermission.objects.filter(secret=secret).count() == 0: return secret
	raise Exception('Could not generate a unique secret')

class AlertPermission(models.Model):
	"""A record of some entity which is allowed to send alerts."""
	name = models.CharField(max_length=128, blank=False, null=False)
	secret = models.CharField(max_length=64, blank=False, null=False, default=create_secret, unique=True)

	def send_alert(self, message, subject=None):
		current_site = Site.objects.get_current()
		rendered_subject = render_to_string('pokepoke/email/alert_subject.txt', { 'subject':subject, 'site': current_site })
		subject = ''.join(rendered_subject.splitlines())
		rendered_message = render_to_string('pokepoke/email/alert.txt', { 'message':message, 'site': current_site })
		send_mail('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, rendered_subject), rendered_message, settings.DEFAULT_FROM_EMAIL, (settings.ALERT_EMAIL_ADDRESS,))
		AlertLog.objects.create(permission=self, subject=subject, message=message)

	def __unicode__(self):
		return '%s' % self.name
	class Meta:
		ordering = ('name',)

class AlertLog(models.Model):
	"""A record of an alert broadcast"""
	created = models.DateField(auto_now_add=True)
	permission = models.ForeignKey(AlertPermission, blank=False, null=False)
	subject = models.CharField(max_length=1024, blank=True, null=True)
	message = models.TextField(blank=True, null=True)
	class Meta:
		ordering = ('-created',)
