from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^info/$', 'phonon.api_views.information_node'),
	(r'^tour-intro/$', 'phonon.api_views.tour_intro'),
	(r'^emergency/$', 'phonon.api_views.emergency_intro'),
	(r'^emergency/code/$', 'phonon.api_views.emergency_code'),
)
