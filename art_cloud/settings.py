import os

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
BACKUP_ROOT = PROJECT_ROOT + '/backups/'

# the directories under the media root which include things like uploaded pics or other dynamic files
DYNAMIC_MEDIA_DIRS = ['photo', 'resized_image', 'wiki_file', 'wiki_photo', 'phonon_audio_clip']

SOUTH_AUTO_FREEZE_APP = True

AUTH_PROFILE_MODULE = "front.UserProfile"

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Vancouver'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

MEDIA_ROOT = PROJECT_ROOT + '/media/'

ADMIN_MEDIA_PREFIX = '/admin-media/'

FORCE_LOWERCASE_TAGS = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p=$i77rnyk76a!_7o1@a)5341k5$r#hddee68(wvog_ozjyc^%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
	'art_cloud.context_processors.site',
	'art_cloud.context_processors.search',
)

ROOT_URLCONF = 'urls'

# absolute paths here, too
TEMPLATE_DIRS = ( PROJECT_ROOT + '/templates/', )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.comments',
	'pagination',
	'tagging',
	'south',
	'piston',
	'art_cloud.clue',
	'art_cloud.front',
	'art_cloud.datonomy',
	'art_cloud.wiki',
	'art_cloud.phonon',
	'art_cloud.pokepoke',
)

from local_settings import *

