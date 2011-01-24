# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback

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
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

from models import *
from forms import AudioEmergencyForm
from incus_client import IncusClient
from hydration import dehydrate_to_xml

@staff_member_required
def index(request):
	try:
		client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
		devices = client.fetch_devices()
	except:
		traceback.print_exc()
		devices = None
	return render_to_response('malleus/index.html', { "devices":devices }, context_instance=RequestContext(request))

def emergency(request):
	page_message = None
	if request.method == 'POST':
		audio_emergency_form = AudioEmergencyForm(request.POST)
		if audio_emergency_form.is_valid():
			try:
				client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
				result = client.activate_emergency_mute(audio_emergency_form.cleaned_data['mute_code'])
				if result == True:
					page_message = 'The emergency mute has been activated.'
				elif result == False:
					page_message = 'That code was not accepted.'
				else:
					page_message = 'There was a problem. Please call the art technician.'
			except:
				page_message = 'There was an error.  Please call the art technician.'
				traceback.print_exc()
			audio_emergency_form = AudioEmergencyForm()
	else:
		audio_emergency_form = AudioEmergencyForm()
	return render_to_response('malleus/emergency.html', { 'page_message':page_message, 'audio_emergency_form':audio_emergency_form }, context_instance=RequestContext(request))

@staff_member_required
def device(request, id):
	try:
		client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
		device = client.fetch_device(id)
	except:
		traceback.print_exc()
		device = None
	return render_to_response('malleus/device.html', { "device":device }, context_instance=RequestContext(request))

@staff_member_required
def channel_group(request, id):
	try:
		client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
		channel_group = client.fetch_group(id)
	except:
		traceback.print_exc()
		channel_group = None
	return render_to_response('malleus/channel_group.html', { "channel_group":channel_group }, context_instance=RequestContext(request))
