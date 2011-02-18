import datetime
import calendar
import pprint
import traceback
import logging

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
from django.core.urlresolvers import reverse

from malleus.incus_client import IncusClient
from models import *

def require_twilio_auth(function):
	"""A decorator which gives the API error if the request doesn't have the proper account guid from Twilio"""
	if not settings.REQUIRE_TWILIO_AUTH: return function
	def _rta(request, *args, **kwargs):
		if request.REQUEST.get('AccountGuid') != settings.TWILIO_ACCOUNT_GUID:
			logging.warn('Received an API call without the twilio account guid')
			return render_to_response('phonon/phone/no_auth.xml', {}, context_instance=RequestContext(request))
		return function(request, *args, **kwargs)
	return _rta

def get_or_create_call(request):
	try:
		if request.REQUEST.get('CallStatus') == 'completed':
			call = PhoneCall.objects.get(guid=request.REQUEST.get('CallGuid'))
			call.completed = datetime.datetime.now()
			call.save()
			return call

		phone = Phone.objects.get_by_number(request.REQUEST.get('Caller'))
		if phone == None:
			phone = Phone.objects.create(phone_number=request.REQUEST.get('Caller'))
			
		if phone.blocked:
			logging.debug('Refusing a blocked phone: %s' % request.REQUEST.get('Caller'))
			return None
			
		return PhoneCall.objects.get_or_create(phone=phone, guid=request.REQUEST.get('CallGuid'))[0]
	except:
		logging.exception('error in intro: %s' % request.REQUEST.get('Caller'))
		traceback.print_exc()
		return None

@require_twilio_auth
def emergency_intro(request):
	call = get_or_create_call(request)
	if call == None: return render_to_response('phonon/phone/error.xml', {'error_message':'Error in emergency intro'}, context_instance=RequestContext(request))
	return render_to_response('phonon/phone/emergency_intro.xml', { }, context_instance=RequestContext(request))

@require_twilio_auth
def emergency_code(request):
	call = get_or_create_call(request)
	if call == None: 
		return render_to_response('phonon/phone/error.xml', {'error_message':'There was an error with the code'}, context_instance=RequestContext(request))

	try:
		if request.method == 'POST' and request.REQUEST.get('Digits', None):
			client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
			result = client.activate_emergency_mute(request.REQUEST.get('Digits'))
			if result == True:
				return render_to_response('phonon/phone/emergency_activated.xml', {}, context_instance=RequestContext(request))
			elif result == False:
				return HttpResponseRedirect(reverse('phonon.api_views.emergency_intro'))
			else:
				return render_to_response('phonon/phone/error.xml', { 'error_message':'There was a problem. Please call the art technician.' }, context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect(reverse('phonon.api_views.emergency_intro'))
	except:
		logging.exception('error in emergency_code: %s' % request.REQUEST.get('Caller'))
		traceback.print_exc()
		return render_to_response('phonon/phone/error.xml', {'error_message':'Error in code two'}, context_instance=RequestContext(request))

@require_twilio_auth
def tour_intro(request):
	"""The root view"""
	logging.debug("%s called %s" % (request.REQUEST.get('Caller', None), request.REQUEST.get('Called', None)))

	call = get_or_create_call(request)
	if call == None: return render_to_response('phonon/phone/error.xml', {}, context_instance=RequestContext(request))

	landing_clip = AudioClip.objects.default_landing_clip()
	if landing_clip != None:
		intro_audio_url = 'http://%s%s' % (Site.objects.get_current().domain, landing_clip.audio.url)
	else:
		intro_audio_url = None

	return render_to_response('phonon/phone/tour_intro.xml', { 'intro_audio_url':intro_audio_url }, context_instance=RequestContext(request))

@require_twilio_auth
def information_node(request):
	"""Information based on a node code"""
	try:
		phone = Phone.objects.get_by_number(request.REQUEST.get('Caller'))
		call = PhoneCall.objects.filter(guid=request.REQUEST.get('CallGuid'))
		if request.method == 'POST' and request.REQUEST.get('Digits', None):
			digits = int(request.REQUEST.get('Digits'))
			if InformationNode.objects.filter(code=digits).count() > 0:
				node = InformationNode.objects.filter(code=digits)[0]
				return render_to_response('phonon/phone/information_node.xml', {'information_node':node }, context_instance=RequestContext(request))
	except:
		logging.exception('error in information code: %s' % request.REQUEST.get('Caller'))
		traceback.print_exc()
		return render_to_response('phonon/phone/error.xml', {}, context_instance=RequestContext(request))
	return HttpResponseRedirect(reverse('phonon.api_views.tour_intro'))
