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
from django.core.urlresolvers import reverse

from models import *
from hydration import *

MAX_LIST_SIZE = 100

def model_list(request, model):
	"""Generates an XML list of models starting at 0 or the parameter 'start'"""
	start = int(request.GET.get('start', 0))
	return HttpResponse(dehydrate_to_list_xml(model.objects.all(), start, start + MAX_LIST_SIZE), mimetype=mime_type(request))

def model(request, id, model):
	"""Generates an XML representation of a model"""
	instance = get_object_or_404(model, pk=id)
	return HttpResponse(dehydrate_to_xml(instance), mime_type(request))

def podo(request, podo):
	"""Generates an XML representation of a plain old django object"""
	return HttpResponse(dehydrate_to_xml(podo()), mime_type(request))

def mime_type(request):	return request.GET.get('mime-type', 'application/xml')
