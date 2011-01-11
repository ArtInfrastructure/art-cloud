# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback

from django.conf import settings
from django.db.models import Q
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseBadRequest
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

def exists(request):
	if request.GET.get('username', None):
		return HttpResponse(User.objects.filter(username=request.GET.get('username')).count() > 0, mimetype='text/plain')
	return HttpResponse('False', mimetype='text/plain')

def auth(request):
	if request.POST.get('username', None) and request.POST.get('password', None):
		if User.objects.filter(username=request.POST.get('username')).count() == 0: return HttpResponse('False', mimetype='text/plain')
		user = User.objects.get(username=request.POST.get('username'))
		return HttpResponse(user.check_password(request.POST.get('password')), mimetype='text/plain')
	return HttpResponse('False', mimetype='text/plain')
