# -*- coding: utf-8 -*-

"""
Updates the context sent to all templates with every request
"""

from django.conf import settings
import django
import sys
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site


def admin_settings(request):
    """Collects settings for the admin"""

    python_version = "%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

    ctx = {
        'MAILHOG_URL': settings.MAILHOG_URL,
        'RABBITMQ_MANAGEMENT_URL': settings.RABBITMQ_MANAGEMENT_URL,
        'SENTRY_URL':  settings.SENTRY_URL,
        'PROJECT_NAME': settings.PROJECT_NAME,
        'django_version': django.get_version(),
        'python_version': python_version,
        'ON_HEROKU': settings.ON_HEROKU,
        'SITE_URL': get_current_site(request),
        'HOST_URL': request.get_host(),
    }

    if request.tenant:
        ctx.update({
            'TENANT_NAME': request.tenant.name,
        })
    if settings.ON_HEROKU:
        ctx.update({
            'HEROKU_RELEASE_CREATED_AT':  datetime.strptime(settings.HEROKU_RELEASE_CREATED_AT, "%Y-%m-%dT%H:%M:%SZ"),
            'HEROKU_RELEASE_VERSION': settings.HEROKU_RELEASE_VERSION,
            'HEROKU_SLUG_COMMIT': settings.HEROKU_SLUG_COMMIT[:8],
            'HEROKU_SLUG_DESCRIPTION': settings.HEROKU_SLUG_DESCRIPTION,
        })

    return ctx
