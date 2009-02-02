# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^photo/(?P<id>[\d]+)/$', 'art_cloud.front.views.photo_detail'),
    (r'^equipment-type/(?P<id>[\d]+)/$', 'art_cloud.front.views.equipment_type_detail'),
    (r'^equipment/(?P<id>[\d]+)/$', 'art_cloud.front.views.equipment_detail'),
    (r'^installation-site/(?P<id>[\d]+)/$', 'art_cloud.front.views.installation_site_detail'),
    (r'^installation/(?P<id>[\d]+)/$', 'art_cloud.front.views.installation_detail'),
    (r'^profile/(?P<username>[^/]+)/$', 'art_cloud.front.views.profile_detail'),
	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'front/login.html'}),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
	(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    (r'^heartbeat/$', 'art_cloud.front.views.heartbeats'),

    (r'^$', 'art_cloud.front.views.index'),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	
)
