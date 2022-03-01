"""WSGI config for orp project."""

# Standard
import os

# Third Party
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'orp_apps.settings.settings'
)

application = get_asgi_application()
