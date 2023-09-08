"""
WSGI config for djangocrud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

setting_module = 'djangocrud.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'djangocrud.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.deployment')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')

application = get_wsgi_application()
