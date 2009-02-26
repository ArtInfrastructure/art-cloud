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
from django.core.urlresolvers import reverse

from models import *
from forms import *

@login_required
def index(request):
	page = WikiPage.objects.get_or_create(name='SplashPage')
	return render_to_response('wiki/index.html', { 'wiki_pages':WikiPage.objects.all(), 'page':page }, context_instance=RequestContext(request))

@login_required
def wiki(request, name):
	page = WikiPage.objects.get_or_create(name=name)
	if not page.id:
		return HttpResponseRedirect(page.get_edit_url())
	return render_to_response('wiki/wiki.html', { 'page':page }, context_instance=RequestContext(request))

@login_required
def wiki_history(request, name):
	return render_to_response('wiki/wiki_history.html', { 'page':WikiPage.objects.get_or_create(name=name) }, context_instance=RequestContext(request))

@login_required
def wiki_page_log(request, name, id):
	page_log = get_object_or_404(WikiPageLog, wiki_page__name=name, pk=id)
	if request.method == 'POST' and request.POST.get('revert', None):
		page_log.wiki_page.content = page_log.content
		page_log.wiki_page.save()
		return HttpResponseRedirect(page_log.wiki_page.get_absolute_url())
	return render_to_response('wiki/wiki_page_log.html', { 'page_log':page_log  }, context_instance=RequestContext(request))

@login_required
def wiki_edit(request, name):
	page = WikiPage.objects.get_or_create(name=name)
	if request.method == 'POST':
		page_form = WikiPageForm(request.POST, instance=page)
		if page_form.is_valid():
			page = page_form.save()
			if request.GET.get('next', None): return HttpResponseRedirect(request.GET.get('next'))
			return HttpResponseRedirect(page.get_absolute_url())
	else:
		page_form = WikiPageForm(instance=page)
	return render_to_response('wiki/wiki_edit.html', { 'page':page, 'page_form':page_form }, context_instance=RequestContext(request))
