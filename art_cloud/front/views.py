# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
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
import django.contrib.contenttypes.models as content_type_models
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import feedgenerator

from models import *
from forms import *

INSTALLATION_ID_PARAMETER = 'installation_id'
INFO_PARAMETER = 'info'
CLEAN_HEARTBEATS_PARAMETER = 'clean_heartbeats'
CHECK_HEARTBEATS_PARAMETER = 'check_heartbeats'

@login_required
def index(request):
	return render_to_response('front/index.html', { 'profiles':UserProfile.objects.filter(user__groups__name="artists"), 
													'sites':InstallationSite.objects.all(), 
													'installations':Installation.objects.all(),
													'artist_groups':ArtistGroup.objects.all(),
													}, context_instance=RequestContext(request))

@login_required
def artist_group_detail(request, id):
	artist_group = get_object_or_404(ArtistGroup, pk=id)
	return render_to_response('front/artist_group_detail.html', { 'artist_group':artist_group }, context_instance=RequestContext(request))

def heartbeats(request):
	if request.GET.has_key(INSTALLATION_ID_PARAMETER):
		id = int(request.GET[INSTALLATION_ID_PARAMETER])
		info = request.GET.get(INFO_PARAMETER, None)
		try:
			installation = Installation.objects.get(pk=id)
			heartbeat = Heartbeat(installation=installation, info=info)
			heartbeat.save()
		except:
			print "Received heartbeat for unknown installation id: %s from IP# %s" % (id, request.META['REMOTE_ADDR'])
	if request.GET.has_key(CLEAN_HEARTBEATS_PARAMETER):
		Heartbeat.objects.delete_old_heartbeats()
	if request.GET.has_key(CHECK_HEARTBEATS_PARAMETER):
		message = ""
		should_send = False
		for installation in Installation.objects.all():
			if installation.is_opened():
				heartbeats = Heartbeat.objects.filter(installation=installation)
				if len(heartbeats) == 0: continue #no heartbeat in days?  ignoring
				if heartbeats[0].timed_out():
					message += 'No heartbeat for %s since %s.\n' % (installation.name, heartbeats[0].created)
					should_send = True
		if should_send:
			UserProfile.objects.notify_art_technician('Art Infrastructure Heartbeat Notice', message)
	return render_to_response('front/heartbeats.html', { 'installations':Installation.objects.all_open(), 'heartbeats':Heartbeat.objects.all() }, context_instance=RequestContext(request))

@login_required
def profile_detail(request, username):
	profile = get_object_or_404(UserProfile, user__username=username)
	if request.method == 'POST' and request.user.is_staff:
		user_form = UserForm(request.POST, instance=profile.user)
		user_profile_form = UserProfileForm(request.POST, instance=profile)
		if user_form.is_valid():
			user_form.save()
		if user_profile_form.is_valid():
			user_profile_form.save()

	profile = get_object_or_404(UserProfile, user__username=username)
	user_form = UserForm(instance=profile.user)
	user_profile_form = UserProfileForm(instance=profile)
	return render_to_response('front/profile_detail.html', { 'profile':profile, 'user_form':user_form, 
															'user_profile_form':user_profile_form }, context_instance=RequestContext(request))

@login_required
def photo_detail(request, id):
	photo = get_object_or_404(Photo, pk=id)
	return render_to_response('front/photo_detail.html', { 'photo':photo }, context_instance=RequestContext(request))

@login_required
def equipment_type_detail(request, id):
	return render_to_response('front/equipment_type_detail.html', {}, context_instance=RequestContext(request))

@login_required
def equipment_detail(request, id):
	return render_to_response('front/equipment_detail.html', {}, context_instance=RequestContext(request))

@login_required
def installation_site_detail(request, id):
	site = get_object_or_404(InstallationSite, pk=id)
	if request.method == 'POST':
		photo_form = PhotoForm(request.POST, request.FILES)
		if photo_form.is_valid():
			photo = photo_form.save()
			site.photos.add(photo)
			site.save()
	else:
		photo_form = PhotoForm()
	return render_to_response('front/installation_site_detail.html', { 'photo_form':photo_form, 'installation_site':site }, context_instance=RequestContext(request))

@login_required
def installation_detail_slug(request, slug):
	installation = get_object_or_404(Installation, slug=slug)
	return common_installation_detail(request, installation)
	
@login_required
def installation_detail(request, id):
	installation = get_object_or_404(Installation, pk=id)
	return common_installation_detail(request, installation)
	
def common_installation_detail(request, installation):
	if request.method == 'POST':
		photo_form = PhotoForm(request.POST, request.FILES)
		if photo_form.is_valid():
			photo = photo_form.save()
			installation.photos.add(photo)
			installation.save()
	else:
		photo_form = PhotoForm()

	return render_to_response('front/installation_detail.html', { 'installation':installation, 'photo_form':photo_form }, context_instance=RequestContext(request))

