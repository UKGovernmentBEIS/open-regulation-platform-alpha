"""Django settings for settings project."""

# Standard
import os
import sys
from pathlib import Path
from typing import List
from warnings import warn

from .drf_settings import *  # noqa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'orp_api',
        'USER': os.environ.get('DB_USER', 'admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'admin'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS: List[str] = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in orp_apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = os.getenv(
    'DJANGO_STATIC_ROOT',
    '/var/opt/orp/settings/static/')

# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/s/orp_apps/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'APP_DIRS': True,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates') # noqa
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


######################################################################
#                        Api Settings                                #


API_URL = 'http://{0}:{1}/'.format(
        os.environ.get('API_HOST', '0.0.0.0'),
        os.environ.get('API_PORT', 3001))

#                        Api Settings end                            #
######################################################################


######################################################################
#                      Swagger Settings                              #
SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'orp_apps.urls.openapi_info',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
#                      Swagger Settings end                          #
######################################################################

ROOT_URLCONF = 'orp_apps.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'drf_yasg',
    'orp_apps.orp_api',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--xunit-file=test_results.xml',
    # Comment out the following line to disable parallelized testing
    # Number of processes to spawn. Negative number means auto based on cores
    '--processes=-2',
    '--process-timeout=120',
]

# Increase the range of ports the Django LiveServerTestCase can spawn on
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8082-8092'

# Logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)8s -- %(message)s - %(name)s:%(lineno)s',
        },
    },
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'

        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'orp_apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


# Try to retrieve local settings.
try:
    # Third Party
    from local_settings import *  # noqa F403
except ImportError:
    pass

# Try to retrieve production settings.
try:
    sys.path.insert(
        0,
        os.getenv(
            'SITE_PATH',
            '/etc/opt/orp/settings/'))
    # Third Party
    from orp_apps_proj_settings import *  # noqa F403
except ImportError:
    pass

# This section will break if the secret key has not been set up, and the
# application is not in DEBUG mode. This likely means that the application
# has been incorrectly deployed.
SECRET_KEY: str
try:
    SECRET_KEY  # noqa F405
except NameError:
    SECRET_KEY_FILE = '/opt/orp/keys/settings.key'
    try:
        with open(SECRET_KEY_FILE) as fd:
            SECRET_KEY = fd.read().strip()
    except IOError:
        if DEBUG:
            # If there's no secret key, and we appear to be in DEBUG mode,
            # allow the situation, but emit a warning.
            warn(
                'Insecure mode: No SECRET_KEY has been set. Allowing '
                'cryptographically weak development application due to DEBUG '
                'being set. THIS MESSAGE SHOULD NEVER APPEAR IN PRODUCTION.'
            )
            SECRET_KEY = 'NOT_VERY_SECRET'
        else:
            raise Exception(
                'Application Insecure. Set up a secret key in {}'.format(
                    SECRET_KEY_FILE
                ))
