import os
import logging
from django.db.utils import OperationalError 
from django.db import connections
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ['SECRET']
# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
ALLOWED_HOSTS = ['https://mycodecave.azurewebsites.net']
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

# Attempt to establish the database connection
try:
    connection = connections['default']
    connection.ensure_connection()
    print("Database connection is successful!")
except OperationalError as e:
    # Handle the connection error
    logging.error(f"Database connection error: {e}")
    print("Database connection failed!")