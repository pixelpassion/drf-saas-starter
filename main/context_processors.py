# -*- coding: utf-8 -*-

"""
Updates the context sent to all templates with every request
"""

import sys
from datetime import datetime

import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

User = get_user_model()


def admin_settings(request):
    """Collects settings for the admin"""

    python_version = "%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

    users = User.objects.select_related('logged_in_user')

    for user in users:
        user.status = 'online' if hasattr(user, 'logged_in_user') else 'offline'
        user.full_name = user.get_full_name()

    site_url = "-"

    try:
        site_url = get_current_site(request)
    except Site.DoesNotExist:
        pass

    ctx = {
        'MAILHOG_URL': settings.MAILHOG_URL,
        'RABBITMQ_MANAGEMENT_URL': settings.RABBITMQ_MANAGEMENT_URL,
        'SENTRY_URL':  settings.SENTRY_URL,
        'PROJECT_NAME': settings.PROJECT_NAME,
        'django_version': django.get_version(),
        'python_version': python_version,
        'ON_HEROKU': settings.ON_HEROKU,
        'SITE_URL': site_url,
        'HOST_URL': request.get_host(),
        'users': users
    }

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
