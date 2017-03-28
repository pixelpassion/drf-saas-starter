# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from main.mixins import UUIDMixin

from django.contrib.sites.models import Site, _simple_domain_name_validator
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.mails.utils import create_and_send_mail


def validate_default_site(value):
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

    name = models.CharField(max_length=100, help_text=_(u"Name of the tenant (the agency or company)"), unique=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this tenant should be treated as active. '),
    )

    date_joined = models.DateTimeField(_('date joined'), help_text=_("When did the user join?"), default=timezone.now)

    site = models.OneToOneField(Site, null=False, blank=False, validators=[validate_default_site, ])

    objects = TenantManager()

    class Meta:
        verbose_name = _('tenant')
        verbose_name_plural = _('tenants')

    def __str__(self):
        return self.name

    def add_user(self, user):
        user.tenants.add(self)

    @property
    def domain(self):
        return "{}://{}".format(settings.DEFAULT_PROTOCOL, self.site.domain)


@receiver(post_delete, sender=Tenant)
def auto_delete_site_with_tenant(sender, instance, **kwargs):
    """ The site will can be deleted, when the tenant is deleted """
    instance.site.delete()


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

    tenant = models.ForeignKey(Tenant, null=False, blank=False, related_name="domains", on_delete=models.CASCADE)

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


class Invite(TenantMixin):

    email = models.EmailField(null=False, blank=False)

    class Meta:
        verbose_name = _('invite')
        verbose_name_plural = _('invites')

    def __str__(self):
        return self.email

    def send_invite(self):

        create_and_send_mail(template="tenants/invite", context={'name': 'Jens'}, to_address=self.email)
