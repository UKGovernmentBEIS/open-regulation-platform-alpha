#!/usr/bin/env python3.8
"""Management script for the application."""
# flake8: noqa
# Standard
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'orp_apps.settings.settings'
    )

    # Third Party
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
