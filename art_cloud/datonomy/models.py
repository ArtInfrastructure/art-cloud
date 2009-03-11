# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import datetime, calendar
import traceback
import logging
import pprint

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class NamedDateManager(models.Manager):
	def get_for_object(self, obj):
		""" Create a queryset matching all NamedDates associated with the given object."""
		return self.filter(content_type__pk=ContentType.objects.get_for_model(obj).pk, object_id=obj.pk)

class NamedDate(models.Model):
	"""A named date"""
	name = models.CharField(max_length=1024, blank=False, null=False)
	date = models.DateField(blank=False, null=False)

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	objects = NamedDateManager()

	@models.permalink
	def get_absolute_url(self): return ('datonomy.views.named_date', (), { 'id':self.id })
	class Meta:
		ordering = ['date']
	def __unicode__(self):
		return "%s: %s" % (self.name, self.date)



