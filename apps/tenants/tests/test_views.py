from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from apps.tenants.models import Domain, Tenant


@override_settings(TENANT_DOMAIN="example.com")
class TenantDomainTests(TestCase):
    """ """

    def setUp(self):
        """ Setup an existing Tenant A with a site subdomain a.example.com and an external domain a.com"""

        self.site = Site.objects.create(name="a.example.com", domain="a.example.com")
        self.tenant = Tenant.objects.create(name="A", site=self.site)
        self.domain = Domain.objects.create(domain="a.com", tenant=self.tenant)

        self.other_site = Site.objects.create(name="other.example.com", domain="other.example.com")
        self.other_tenant = Tenant.objects.create(name="Other", site=self.other_site)
        self.other_domain = Domain.objects.create(domain="other.com", tenant=self.other_tenant)

        self.marketing_page = Site.objects.create(name="Marketingpage", domain="landingpage.com")

        self.site_not_linked = Site.objects.create(name="notlinked.example.com", domain="notlinked.example.com")
        
        self.home_url = reverse("home")
        self.secret_url = reverse("tenants:dashboard")

    def test_tenant_root_domain_should_be_accessible(self):
        """ The marketing page should be accessible """

        response = self.client.get(self.home_url, HTTP_HOST="example.com")
        self.assertEquals(response.status_code, 200)

    def test_tenant_marketing_domain_should_be_accessible(self):
        """ The marketing page should be accessible """

        response = self.client.get(self.home_url, HTTP_HOST=self.marketing_page)
        self.assertEquals(response.status_code, 200)

    def test_tenant_domain_should_be_accessible(self):
        """ The tenants subdomain (e.g. a.example.com) should be accessible """

        response = self.client.get(self.home_url, HTTP_HOST=self.site.domain)
        self.assertEquals(response.status_code, 200)

    def test_tenant_external_domain_should_be_accessible(self):
        """ The tenants external domain (e.g. a.com) should be accessible """

        response = self.client.get(self.home_url, HTTP_HOST=self.domain.domain)
        self.assertEquals(response.status_code, 200)

    def test_tenant_not_existing_domain_should_give_not_found_error(self):
        """ An not-existing root domain name should throw an error """

        response = self.client.get(self.home_url, HTTP_HOST='notexisting.com')
        self.assertEquals(response.status_code, 404)

    def test_tenant_not_existing_site_should_give_not_found_error(self):
        """ A non-existing subdomain of the tenant root domain should throw an error """

        response = self.client.get(self.home_url, HTTP_HOST='notexisting.example.com')
        self.assertEquals(response.status_code, 404)

    def test_tenant_not_linked_site_should_give_not_found_error(self):
        """ An existing site without a tenant should throw an error """

        response = self.client.get(self.home_url, HTTP_HOST=self.site_not_linked.domain)
        self.assertEquals(response.status_code, 404)

    def test_tenant_secret_page_on_root_domain_should_not_be_accessible(self):
        """ The marketing page should be accessible """

        response = self.client.get(self.secret_url, HTTP_HOST="example.com")
        self.assertEquals(response.status_code, 403)


    def test_tenant_secret_page_on_marketing_domain_should_not_be_accessible(self):
        """ The marketing page should be accessible """

        response = self.client.get(self.secret_url, HTTP_HOST="landingpage.com")
        self.assertEquals(response.status_code, 403)


    def test_tenant_secret_page_on_other_site_domain_should_not_be_accessible(self):
        """ The tenants subdomain (e.g. a.example.com) should be accessible """

        response = self.client.get(self.secret_url, HTTP_HOST=self.other_site.domain)
        self.assertEquals(response.status_code, 403)


    def test_tenant_secret_page_on_other_external_domain_should_not_be_accessible(self):
        """ The tenants external domain (e.g. a.com) should be accessible """

        response = self.client.get(self.secret_url, HTTP_HOST=self.other_domain.domain)
        self.assertEquals(response.status_code, 403)


    def test_tenant_secret_page_on_not_existing_domain_should_still_give_not_found_error(self):
        """ An not-existing root domain name should throw an error """

        response = self.client.get(self.secret_url, HTTP_HOST='notexisting.com')
        self.assertEquals(response.status_code, 404)


    def test_tenant_secret_page_on_not_existing_site_should_give_not_found_error(self):
        """ A non-existing subdomain of the tenant root domain should throw an error """

        response = self.client.get(self.secret_url, HTTP_HOST='notexisting.example.com')
        self.assertEquals(response.status_code, 404)

    def test_tenant_secret_page_on_not_linked_site_should_give_not_found_error(self):
        """ An existing site without a tenant should throw an error """

        response = self.client.get(self.secret_url, HTTP_HOST=self.site_not_linked.domain)
        self.assertEquals(response.status_code, 404)
