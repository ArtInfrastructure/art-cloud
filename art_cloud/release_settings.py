DEVEL_ROOT = '/webapp/art-cloud/art_cloud'

PRODUCTION = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

#CACHE_BACKEND = 'dummy:///'
CACHE_BACKEND = 'locmem:///'

DATABASE_ENGINE = 'postgresql_psycopg2' 
DATABASE_NAME = 'artcloud'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

MEDIA_ROOT = DEVEL_ROOT + '/media/'
TEMPLATE_DIRS = ( DEVEL_ROOT + '/templates/', )
