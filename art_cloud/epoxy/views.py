import traceback
import httplib2

from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

def go(request):
	conn = httplib2.Http()
	remote_path = request.path[len(reverse('epoxy.views.go')):]
	headers = {'x-epoxy-remote':request.META.get('REMOTE_ADDR', None)}
	if request.method == 'GET':
		url = '%s%s?%s' % (settings.ART_SERVER_EPOXY_URL, remote_path, request.GET.urlencode())
		response, content = conn.request(url, method=request.method, headers=headers)
	elif request.method == 'POST':
		url = '%s%s' % (settings.ART_SERVER_EPOXY_URL, remote_path)
		response, content = conn.request(url, method=request.method, headers=headers, body=request.POST.urlencode())
	return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])

# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
