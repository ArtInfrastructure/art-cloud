# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
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

from tagging.models import Tag, TaggedItem
from datonomy.models import NamedDate
from datonomy.forms import *
from models import *
from forms import *

INSTALLATION_ID_PARAMETER = 'installation_id'
INFO_PARAMETER = 'info'
CLEAN_HEARTBEATS_PARAMETER = 'clean_heartbeats'
CHECK_HEARTBEATS_PARAMETER = 'check_heartbeats'

@login_required
def installation_slice(request): return common_slice(request, 'front/installation_slice.html')

@login_required
def artist_slice(request): return common_slice(request, 'front/artist_slice.html')

@login_required
def site_slice(request): return common_slice(request, 'front/site_slice.html')

def common_slice(request, template):
	return render_to_response(template, { 'profiles':UserProfile.objects.filter(user__groups__name="artists"), 
													'sites':InstallationSite.objects.all(), 
													'installations':Installation.objects.all(),
													'artist_groups':ArtistGroup.objects.all(),
													}, context_instance=RequestContext(request))

@login_required
def search(request):
	installation_results = None
	artist_results = None
	artist_group_results = None
	if request.method == 'POST':
		search_form = SearchForm(request.POST)
		if search_form.is_valid():
			installation_results = Installation.objects.search(search_form.cleaned_data['terms'])
			artist_results = UserProfile.objects.search(search_form.cleaned_data['terms'])
			artist_group_results = ArtistGroup.objects.search(search_form.cleaned_data['terms'])
	else:
		search_form = SearchForm()
	return render_to_response('front/search.html', { 'artist_group_results': artist_group_results, 'artist_results': artist_results, 'installation_results':installation_results, 'search_form': search_form }, context_instance=RequestContext(request))

@login_required
def tags(request):
	return render_to_response('front/tags.html', { }, context_instance=RequestContext(request))

@login_required
def tag(request, name):
	tag = get_object_or_404(Tag, name=name)
	return render_to_response('front/tag.html', { 'tag':tag, 'installations':TaggedItem.objects.get_by_model(Installation, tag) }, context_instance=RequestContext(request))

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
def installation_heartbeats(request, id):
	installation = get_object_or_404(Installation, pk=id)
	return render_to_response('front/installation_heartbeats.html', { 'installation':installation }, context_instance=RequestContext(request))

@login_required
def installation_heartbeats_csv(request, id):
	import csv
	installation = get_object_or_404(Installation, pk=id)

	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=heartbeats.csv'
	writer = csv.writer(response)
	for heartbeat in installation.heartbeat_set.all(): writer.writerow([heartbeat.created, heartbeat.info])

	return response

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
	equipment_type = get_object_or_404(EquipmentType, pk=id)
	default_notes_data = { 'notes': equipment_type.notes }
	if request.method == 'POST':
		equipment_type_notes_form = NotesForm(request.POST)
		if request.POST.get('equipment_type_form_id', None):
			equipment_type.notes = request.POST.get('notes', None)
			equipment_type.save()
	else:
		equipment_type_notes_form = NotesForm(default_notes_data)
	return render_to_response('front/equipment_type_detail.html', { 'equipment_type':equipment_type, 'equipment_type_notes_form':equipment_type_notes_form }, context_instance=RequestContext(request))

@login_required
def equipment_detail(request, id):
	equipment = get_object_or_404(Equipment, pk=id)
	default_notes_data = { 'notes': equipment.notes }
	if request.method == 'POST':
		equipment_notes_form = NotesForm(request.POST)
		if request.POST.get('equipment_form_id', None):
			equipment.notes = request.POST.get('notes', None)
			equipment.save()
	else:
		equipment_notes_form = NotesForm(default_notes_data)
	return render_to_response('front/equipment_detail.html', { 'equipment':equipment, 'equipment_notes_form':equipment_notes_form }, context_instance=RequestContext(request))

@login_required
def installation_site_detail(request, id):
	error_message = None
	site = get_object_or_404(InstallationSite, pk=id)
	if request.method == 'POST':
		photo_form = PhotoForm(request.POST, request.FILES)
		if photo_form.is_valid():
			try:
				photo = photo_form.save()
				site.photos.add(photo)
				site.save()
			except:
				error_message = 'I could not save that photo.'
		else:
			error_message = 'I could not read that photo file.'
	else:
		photo_form = PhotoForm()
	print error_message
	return render_to_response('front/installation_site_detail.html', { 'error_message':error_message, 'photo_form':photo_form, 'installation_site':site }, context_instance=RequestContext(request))

@login_required
def installation_detail_slug(request, slug):
	installation = get_object_or_404(Installation, slug=slug)
	return common_installation_detail(request, installation)
	
@login_required
def installation_detail(request, id):
	installation = get_object_or_404(Installation, pk=id)
	return common_installation_detail(request, installation)
	
def common_installation_detail(request, installation):
	error_message = None
	tag_default_data = {'tags': installation.tag_names }
	notes_default_date = { 'notes':installation.notes }
	if request.method == 'POST':
		photo_form = PhotoForm(request.POST, request.FILES)
		tags_form = TagsForm(request.POST)
		named_date_form = NamedDateForm(request.POST)
		installation_notes_form = NotesForm(request.POST)
		if request.POST.get('photo-form', None):
			tags_form = TagsForm(tag_default_data)
			named_date_form = NamedDateForm()
			installation_notes_form = NotesForm(notes_default_date)
			if photo_form.is_valid():
				try:
					photo = photo_form.save()
					installation_notes_form = NotesForm(notes_default_date)
					installation.photos.add(photo)
					installation.save()
				except:
					error_message = 'I could not read that photo file.'
			else:
				error_message = 'I could not read that photo.'
		elif request.POST.get('recent_dates', None):
			tags_form = TagsForm(tag_default_data)
			photo_form = PhotoForm()
			installation_notes_form = NotesForm(notes_default_date)
			named_date_form = NamedDateForm()
			dates = [int(rd) for rd in request.POST.getlist('recent_dates')]
			for rd in dates:
				try:
					recent_date = NamedDate.objects.get(pk=rd)
					NamedDate(name=recent_date.name, date=recent_date.date, content_object=installation).save()
				except:
					error_message = 'Could not add that date due to system error.'
					logging.error("Tried to add an unknown NamedDate: %s" % rd)
		elif request.POST.get('named-date-form', None):
			tags_form = TagsForm(tag_default_data)
			photo_form = PhotoForm()
			installation_notes_form = NotesForm(notes_default_date)
			if named_date_form.is_valid():
				pk = named_date_form.cleaned_data['pk']
				if pk:
					date = NamedDate.objects.get(pk=pk)
					date.name = named_date_form.cleaned_data['name']
					date.date = named_date_form.cleaned_data['date']
					date.save()
				else:
					date = named_date_form.save(commit=False)
					date.content_object = installation
					date.save()
				named_date_form = NamedDateForm()
			else:
				print request.POST
				if request.POST.get('id_name', None):
					error_message = 'Could not parse that date.'
				else:
					error_message = 'That date needs a name.'
		elif request.POST.get('installation_form_id', None):
			tags_form = TagsForm(tag_default_data)
			photo_form = PhotoForm()
			named_date_form = NamedDateForm()
			installation.notes = request.POST.get('notes', None)
			installation.save()
		elif request.POST.get('tag-form', None):
			named_date_form = NamedDateForm()
			installation_notes_form = NotesForm(notes_default_date)
			photo_form = PhotoForm()
			if tags_form.is_valid():
				installation.tags = tags_form.cleaned_data['tags']
				installation.save()
				tag_form = TagsForm({'tags': installation.tag_names })
	else:
		installation_notes_form = NotesForm(notes_default_date)
		tags_form = TagsForm(tag_default_data)
		photo_form = PhotoForm()
		named_date_form = NamedDateForm()
	return render_to_response('front/installation_detail.html', { 'error_message':error_message, 'installation':installation, 'recent_dates':NamedDate.objects.all().order_by('-id'), 'can_edit_dates':True, 'named_date_form':named_date_form, 'installation_notes_form':installation_notes_form, 'tags_form': tags_form, 'installation_photo_form':photo_form }, context_instance=RequestContext(request))

