from datetime import timedelta

from django.conf import settings
from django.contrib.sites.models import Site, _simple_domain_name_validator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from main.mixins import UUIDMixin
from ..mails.utils import create_and_send_mail


def validate_default_site(value):
    """This validates the given Site - the default Site can not be used for a tenant.

    TODO: Check, if the site URL is part of TENANT_ROOT_DOMAIN root
    """

    tenant_root_domain = Tenant.objects.get_tenant_root_domain()
    tenant_domain_site_id = Site.objects.get(domain=tenant_root_domain).id

    if value == tenant_domain_site_id:
        raise ValidationError(f'The root domain {{tenant_root_domain}}can not be used.')


class TenantManager(models.Manager):
    use_in_migrations = True

    def create_tenant(self, user, name, subdomain):

        tenant_root_domain = Tenant.objects.get_tenant_root_domain()
        domain = "{}.{}".format(subdomain, tenant_root_domain)

        try:
            Site.objects.get(domain=domain)
            raise ValidationError(f'The domain {{domain}} is already used by another tenant.')
        except Site.DoesNotExist:
            site = Site.objects.create(name=domain, domain=domain)

        tenant = Tenant.objects.create(name=name, site=site)
        tenant.add_user(user)

        return tenant

    def get_tenant_root_domain(self):
        """Return the current Site based on the TENANT_ROOT_SITE_ID in the project's settings.

        If TENANT_ROOT_SITE_ID isn't defined, return an error
        """

        from django.conf import settings
        if getattr(settings, 'TENANT_ROOT_SITE_ID', ''):
            tenant_root_site_id = settings.TENANT_ROOT_SITE_ID
            site = Site.objects.get(pk=tenant_root_site_id)
            return site.domain

        raise ImproperlyConfigured("You're using the Tenant model without having TENANT_ROOT_SITE_ID setting."
                                   " It should be set to the root Site for tenant subdomains ")


class Tenant(UUIDMixin):
    """The Tenant is the client on the platform."""

    name = models.CharField(max_length=100, help_text=_(u"Name of the tenant (the agency or company)"), unique=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this tenant should be treated as active. '),
    )

    date_joined = models.DateTimeField(_('date joined'), help_text=_("When did the tenant join?"), default=timezone.now)

    site = models.OneToOneField(
        Site,
        null=False,
        blank=False,
        validators=[validate_default_site, ],
        on_delete=models.CASCADE
    )

    objects = TenantManager()

    class Meta:
        verbose_name = _('tenant')
        verbose_name_plural = _('tenants')

    def __str__(self):
        return self.name

    def add_user(self, user):
        from apps.users.models import UserTenantRelationship
        UserTenantRelationship.objects.create(user=user, tenant=self)

    @property
    def subdomain(self):
        return "{}://{}".format(settings.DEFAULT_PROTOCOL, self.site.domain)


@receiver(post_delete, sender=Tenant)
def auto_delete_site_with_tenant(sender, instance, **kwargs):
    """The site will be deleted, when the tenant is deleted."""
    instance.site.delete()


class Domain(models.Model):
    """Every tenant can have several extra-domains leading to his site subdomain."""

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
    """A mixin for models to be part of a Tenant."""
    tenant = models.ForeignKey(Tenant, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Invite(TenantMixin, UUIDMixin):
    """An invite to join a tenant."""

    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("inviter"),
        help_text=_("Who invited the person?"),
        related_name='invites_created',
        null=True,
        on_delete=models.SET_NULL,
    )

    email = models.EmailField(
        _('email address'),
        help_text=_("Email of the invitee"),
        null=False,
        blank=False
    )

    first_name = models.CharField(
        _('first name'),
        help_text=_("First Name of the invitee"),
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        _('last name'),
        help_text=_("Last Name of the invitee"),
        max_length=30,
        blank=True,
    )

    time_created = models.DateTimeField(
        _("creation time"),
        help_text=_("When was the invite created?"),
        default=timezone.now,
        editable=False,
    )

    first_clicked = models.DateTimeField(
        _("first clicked"),
        help_text=_("When was the first time the invitee clicked on the invite?"),
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("connected user"),
        help_text=_("Which user was created or connected from invite?"),
        related_name='invites_used',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('invite')
        verbose_name_plural = _('invites')

    def __str__(self):
        return self.email

    @property
    def existing_user_or_invite_used(self):
        """Return a tuple existing_user, invite_used.

        The value of existing_user is only applicable when invite_used is False.
        """
        if not self.user:
            from ..users.models import User
            try:
                existing_user = User.objects.get(email=self.email)
                return existing_user, False
            except User.DoesNotExist:
                return None, False
        return None, True

    # TODO Generate the absolute URI for email (how does rest_auth do it?)
    def get_activation_url(self):
        path = reverse('rest_invite_activation', kwargs={'tenant_name': self.tenant.name, 'pk': self.pk})
        return path

    def send_invite(self):
        create_and_send_mail(
            template_name="invite",
            context={
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'tenant_name': self.tenant.name,
                'inviter_first_name': self.inviter.first_name,
                'inviter_last_name': self.inviter.last_name,
                'inviter_email': self.inviter.email,
                'activation_uri': self.get_activation_url()
            },
            to_address=self.email
        )

    @property
    def is_active(self):
        return timezone.now() - self.time_created < timedelta(days=settings.TENANT_INVITE_EXPIRATION_IN_DAYS)
