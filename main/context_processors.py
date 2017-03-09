# -*- coding: utf-8 -*-

"""
Updates the context sent to all templates with every request
"""

from django.conf import settings


def admin_settings(request):
    """Collects settings for the admin"""

    return {
        'MAILHOG_URL': settings.MAILHOG_URL,
        'RABBITMQ_MANAGEMENT_URL': settings.RABBITMQ_MANAGEMENT_URL,
        'SENTRY_URL':  settings.SENTRY_URL,
        'PROJECT_NAME': settings.PROJECT_NAME,
    }