# -*- coding: utf-8 -*-

""" Mixins for the API """

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreateMixin(models.Model):
    """Stores timestamps for creation."""

    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        """ """
        abstract = True
        get_latest_by = 'created'
        ordering = ('created',)


class CreateUpdateMixin(CreateMixin):
    """Stores timestamps for creation AND last modification."""

    updated = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        """ """
        abstract = True


class ValidFromUntilMixin(models.Model):
    """Stores timestamps for creation AND last modification."""

    valid_from_inclusive = models.DateField(_('valid_from'), auto_now_add=True, null=False, blank=False)
    valid_until_exclusive = models.DateField(_('valid until'), null=True, blank=True)

    class Meta:
        """ """
        abstract = True


class UUIDMixin(models.Model):
    """Stores timestamps for creation AND last modification."""

    id = models.UUIDField(_('ID'), primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        """ """
        abstract = True

