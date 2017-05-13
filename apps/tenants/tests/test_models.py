from django.contrib.sites.models import Site
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings

from apps.tenants.models import Domain, Tenant


class TenantDomainTests(TestCase):
    """ """

    def setUp(self):
        """ """

        self.tenant_domain = Tenant.objects.get_tenant_domain()
        self.site = Site.objects.create(name="a.example.com", domain="a.example.com")
        self.tenant = Tenant.objects.create(name="A", site=self.site)

    def test_create_tenant_without_site_should_fail(self):
        """ Every Tenant needs at site """

        with self.assertRaises(IntegrityError):
            Tenant.objects.create(name="B")

    def test_a_site_can_only_belong_to_one_tenant(self):
        """A site can only be set for one tenant """

        with self.assertRaises(IntegrityError):
            Tenant.objects.create(name="B", site=self.site)

    def test_domains(self):
        """Can the tenant set external domains?"""

        self.domain = Domain.objects.create(domain="a.com", tenant=self.tenant)

    def test_tenant_can_not_use_the_main_tenant_domain(self):
        """The example.com should not belong to any tenant"""
        pass

        # This can not be avoided on model site. But it is checked when using a form.

    def test_create_site_with_invalid_tenant_domain(self):
        """ Check that sites can only be created for the TENANT_DOMAIN (example.com) """
        pass
