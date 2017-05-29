"""
Updates the context sent to all templates with every request
"""

import sys
import os
from datetime import datetime

import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()


def admin_settings(request):
    """Collects settings for the admin"""

    python_version = "%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

    logged_in_users = User.objects.exclude(signed_in=None)

    site_url = "-"

    try:
        site_url = get_current_site(request)
    except Site.DoesNotExist:
        pass

    ctx = {
        'MAILHOG_MANAGEMENT_URL': settings.MAILHOG_MANAGEMENT_URL,
        'RABBITMQ_MANAGEMENT_URL': settings.RABBITMQ_MANAGEMENT_URL,
        'SENTRY_MANAGEMENT_URL':  settings.SENTRY_MANAGEMENT_URL,
        'PROJECT_NAME': settings.PROJECT_NAME,
        'django_version': django.get_version(),
        'python_version': python_version,
        'ON_HEROKU': settings.ON_HEROKU,
        'SITE_URL': site_url,
        'HOST_URL': request.get_host(),
        'logged_in_users': logged_in_users
    }

    SENTRY_DSN = os.environ.get('SENTRY_DSN', None)

    if SENTRY_DSN:
        ctx.update({
            'SENTRY_DSN': SENTRY_DSN,
        })

    if hasattr(request, "tenant") and request.tenant:
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
