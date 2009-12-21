# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings

from piston.resource import Resource
from handlers import WeatherHandler, AirportObservationHandler

from models import *

weather_resource = Resource(handler=WeatherHandler)
airport_observation_resource = Resource(handler=AirportObservationHandler)

urlpatterns = patterns('',
   url(r'^api/weather/(?P<zip_code>[\d]+).xml$', weather_resource, { 'emitter_format': 'xml' }), 
   url(r'^api/weather/airport/(?P<airport_code>[^/]+).xml$', airport_observation_resource, { 'emitter_format': 'string2xml' }), 

	(r'^photo/(?P<id>[\d]+)/$', 'art_cloud.front.views.photo_detail'),
	(r'^equipment-type/(?P<id>[\d]+)/$', 'art_cloud.front.views.equipment_type_detail'),
	(r'^equipment/(?P<id>[\d]+)/$', 'art_cloud.front.views.equipment_detail'),
	(r'^installation-site/(?P<id>[\d]+)/$', 'art_cloud.front.views.installation_site_detail'),
	(r'^installation/(?P<id>[\d]+)/$', 'art_cloud.front.views.installation_detail'),
	(r'^installation/(?P<id>[\d]+)/heartbeat/$', 'art_cloud.front.views.installation_heartbeats'),
	(r'^installation/(?P<id>[\d]+)/heartbeat/csv/$', 'art_cloud.front.views.installation_heartbeats_csv'),
	(r'^installation/(?P<slug>[^/]+)/$', 'art_cloud.front.views.installation_detail_slug'),
	(r'^profile/(?P<username>[^/]+)/$', 'art_cloud.front.views.profile_detail'),
	(r'^tag/(?P<name>[^/]+)/$', 'art_cloud.front.views.tag'),
	(r'^tag/$', 'art_cloud.front.views.tags'),
	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'front/login.html'}),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
	(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	(r'^heartbeat/$', 'art_cloud.front.views.heartbeats'),
	(r'^group/(?P<id>[\d]+)$', 'art_cloud.front.views.artist_group_detail'),
	(r'^search/$', 'art_cloud.front.views.search'),

	(r'^installation-slice/$', 'art_cloud.front.views.installation_slice'),
	(r'^artist-slice/$', 'art_cloud.front.views.artist_slice'),
	(r'^$', 'art_cloud.front.views.site_slice'),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
