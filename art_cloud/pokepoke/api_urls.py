from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^alert/$', 'pokepoke.api_views.alert'),
)
