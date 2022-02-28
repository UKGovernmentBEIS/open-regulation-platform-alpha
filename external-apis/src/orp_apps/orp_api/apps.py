"""Apps module for the orp_api app."""
# Third Party
from django.apps import AppConfig


class OrpApiConfig(AppConfig):
    """Configuration for application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orp_apps.orp_api'
