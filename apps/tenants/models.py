# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from main.mixins import UUIDMixin

from django.contrib.sites.models import Site, _simple_domain_name_validator


def validate_default_site_url(value):
    """ This validates the given Site - the default Site can not be used for a tenant

        TODO: Check, if the site URL is part of TENANT_DOMAIN root

    """

    if not hasattr(settings, 'TENANT_DOMAIN'):
        raise ImproperlyConfigured("TENANT_DOMAIN is not set - its the root domain of all tenants basic domains")

    tenant_domain_site_id = Site.objects.get(domain=settings.TENANT_DOMAIN).id

    if value == tenant_domain_site_id:
        raise ValidationError(
            _('The root domain can not be used.').format(value)
        )


class TenantManager(models.Manager):
    use_in_migrations = True

    def create_tenant(self, user, name, domain):

        domain = "{}.{}".format(domain, settings.TENANT_DOMAIN)
        site = Site.objects.create(name=domain, domain=domain)
        tenant = Tenant.objects.create(name=name, site=site)
        user.tenants.add(tenant)

        return tenant


class Tenant(UUIDMixin):
    """
        The Tenant is the client on the platform.
    """

    name = models.CharField(max_length=100, unique=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this tenant should be treated as active. '),
    )

    date_joined = models.DateTimeField(_('date joined'), help_text=_("When did the user join?"), default=timezone.now)

    site = models.OneToOneField(Site, null=False, blank=False, validators=[validate_default_site_url])

    objects = TenantManager()

    class Meta:
        verbose_name = _('tenant')
        verbose_name_plural = _('tenants')

    def __str__(self):
        return self.name


class Domain(models.Model):
    """
        Every tenant can have several extra-domains leading to his site subdomain.
    """
    domain = models.CharField(
        _('domain name'),
        max_length=100,
        validators=[_simple_domain_name_validator],
        unique=True,
    )
    name = models.CharField(_('display name'), max_length=50)

    tenant = models.OneToOneField(Tenant, null=False, blank=False)

    class Meta:
        verbose_name = _('domain')
        verbose_name_plural = _('domains')
        ordering = ('domain',)

    def __str__(self):
        return self.domain

    def natural_key(self):
        return (self.domain,)


class TenantMixin(models.Model):

    tenant = models.ForeignKey(Tenant, null=False, blank=False)

    class Meta:
        abstract = True