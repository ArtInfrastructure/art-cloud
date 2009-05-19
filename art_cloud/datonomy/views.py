# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

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
from django.core import serializers

import vobject

from models import *

@login_required
def recent_dates(request):
	data = serializers.serialize("json", NamedDate.objects.all()[:20])
	return HttpResponse(data, mimetype="application/json")

def ical(request):
	"""The iCal feed view"""
	cal = vobject.iCalendar()
	cal.add('METHOD').value = 'PUBLISH'
	cal.add('X-WR-CALNAME').value = '%s Calendar' % Site.objects.get_current().name
	for named_date in NamedDate.objects.all():
		vevent = cal.add('vevent')
		vevent.add('uid').value = 'named-date-%s' % named_date.id
		vevent.add('summary').value = "%s: %s" % (named_date.content_object, named_date.name)
		vevent.add('description').value = ''
		vevent.add('location').value = ''
		vevent.add('class').value = 'PUBLIC'
		vevent.add('status').value = 'CONFIRMED'
		vevent.add('dtstart').value = datetime.date(named_date.date.year, named_date.date.month, named_date.date.day)
		vevent.add('dtend').value = datetime.date(named_date.date.year, named_date.date.month, named_date.date.day)
	if request.GET.get('test', None):
		response = HttpResponse(cal.serialize(), mimetype='text/plain')
	else:
		response = HttpResponse(cal.serialize(), mimetype='text/calendar')
		response['Filename'] = 'filename.ics'  # IE needs this
		response['Content-Disposition'] = 'attachment; filename=filename.ics'
	return response

@login_required
def calendar(request):
	return calendar_by_date(request, year=datetime.datetime.now().year, month=datetime.datetime.now().month)

@login_required
def calendar_by_date(request, year=datetime.datetime.now().year, month=datetime.datetime.now().month):
	date = datetime.datetime(day=1, month=int(month), year=int(year))
	prev_date = date - datetime.timedelta(days=5)
	prev_date = datetime.datetime(day=1, month=prev_date.month, year=prev_date.year)
	next_date = date + datetime.timedelta(days=31)
	next_date = datetime.datetime(day=1, month=next_date.month, year=next_date.year)
	return render_to_response('datonomy/calendar.html', { 'year':year, 'month':month, 'date':date, 'next_date':next_date, 'prev_date':prev_date }, context_instance=RequestContext(request))

@login_required
def named_date(request, id):
	date = get_object_or_404(NamedDate, pk=id)
	action = request.GET.get('action', None)
	if action == 'delete': date.delete()
	return HttpResponseRedirect(date.content_object.get_absolute_url())

@login_required
def datonomy_js(request):
	return render_to_response('datonomy/datonomy.js', { 'recent_dates':NamedDate.objects.all()[:10] }, context_instance=RequestContext(request), mimetype="text/javascript")


	