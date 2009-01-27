from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^photo/(?P<id>[\d]+)/$', 'art_cloud.front.views.photo_detail'),
    (r'^equipment-type/(?P<id>[\d]+)/$', 'art_cloud.front.views.equipment_type_detail'),
    (r'^equipment/(?P<id>[\d]+)/$', 'art_cloud.front.views.equipment_detail'),
    (r'^installation-site/(?P<id>[\d]+)/$', 'art_cloud.front.views.installation_site_detail'),
    (r'^installation/(?P<id>[\d]+)/$', 'art_cloud.front.views.installation_detail'),
    (r'^profile/(?P<username>[^/]+)/$', 'art_cloud.front.views.profile_detail'),
    (r'^$', 'art_cloud.front.views.index'),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
