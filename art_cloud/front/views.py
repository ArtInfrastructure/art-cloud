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

@login_required
def index(request):
	return render_to_response('front/index.html', { 'profiles':UserProfile.objects.filter(user__groups__name="artists"), 
													'sites':InstallationSite.objects.all(), 
													'installations':Installation.objects.all(),
													}, context_instance=RequestContext(request))

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
	print dir(site)
	return render_to_response('front/installation_site_detail.html', { 'site':site }, context_instance=RequestContext(request))

@login_required
def installation_detail(request, id):
	installation = get_object_or_404(Installation, pk=id)
	return render_to_response('front/installation_detail.html', { 'installation':installation }, context_instance=RequestContext(request))

