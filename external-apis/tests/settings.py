"""Test settings for the project."""
# Standard
import os

# Project
from orp_apps.settings.settings import *  # noqa F403

# overwrite single settings for the testsuite
DEBUG = True

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ()  # noqa F405
API_URL = 'http://localhost:8000/'
API_USERNAME = 'admin'
API_PASSWORD = 'password'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv(
            'DJANGO_SQLITE_PATH',
            ('/var/opt/orp/settings'
             '/db/settings.sqlite')
        ),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
