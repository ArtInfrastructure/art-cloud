from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^info/$', 'phonon.api_views.information_node'),
	(r'^intro/$', 'phonon.api_views.intro'),
)
