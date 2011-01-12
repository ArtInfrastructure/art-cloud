# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback
import logging
import urllib
import sys

from django.conf import settings
from django.db.models import Q
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.utils.html import strip_tags
import django.contrib.contenttypes.models as content_type_models
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import feedgenerator

from incus_client import IncusClient
from hydration import dehydrate_to_xml, hydrate_from_xml

@staff_member_required
def channel_gain(request, id):
	try:
		client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
		if request.method == 'POST' and request.POST.get('gain', None):
			gain = client.set_channel_gain(id, float(request.POST.get('gain')))
		else:
			gain = client.get_channel_gain(id)
		if gain == None: raise HttpResponseServerError('Did not receive gain from the art server')
		return HttpResponse(gain, content_type="text/plain")
	except:
		traceback.print_exc()
		raise HttpResponseServerError('Error communicating with the art server', traceback)

@staff_member_required
def channel_group_gain(request, id):
	try:
		client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
		if request.method == 'POST' and request.POST.get('gain', None):
			gain = client.set_group_gain(id, float(request.POST.get('gain')))
		else:
			gain = client.get_group_gain(id)
		if gain == None: raise HttpResponseServerError('Did not receive gain from the art server')
		return HttpResponse(gain, content_type="text/plain")
	except:
		traceback.print_exc()
		raise HttpResponseServerError('Error communicating with the art server', traceback)
