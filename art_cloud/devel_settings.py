DEVEL_ROOT = '/Users/trevor/Documents/San Jose Airport/Site/art-cloud/art_cloud'

PRODUCTION = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

#CACHE_BACKEND = 'dummy:///'
CACHE_BACKEND = 'locmem:///'

DATABASE_ENGINE = 'mysql' 
DATABASE_NAME = 'artcloud'
DATABASE_USER = 'trevor'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

MEDIA_ROOT = DEVEL_ROOT + 'media/'

TEMPLATE_DIRS = ( DEVEL_ROOT + 'templates/', )
