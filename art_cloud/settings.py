# Django settings for art cloud project.

HEARTBEAT_TIMEOUT = 10 # in seconds

ADMINS = (
    ('Trevor F. Smith', 'trevor@trevor.smith.name'),
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = "front.UserProfile"

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Vancouver'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

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

TEMPLATE_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.admin',
	'pagination',
	'tagging',
	'art_cloud.front',
	'art_cloud.datonomy',
	'art_cloud.wiki',
)

from local_settings import *

