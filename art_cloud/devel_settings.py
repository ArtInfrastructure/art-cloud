
ADMINS = (
    ('Trevor F. Smith', 'trevor@trevor.smith.name'),
)
MANAGERS = ADMINS

PRODUCTION = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

#CACHE_BACKEND = 'dummy:///'
CACHE_BACKEND = 'locmem:///'

DATABASE_ENGINE = 'postgresql_psycopg2' 
DATABASE_NAME = 'artcloud'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '1234'
DATABASE_HOST = ''
DATABASE_PORT = ''
