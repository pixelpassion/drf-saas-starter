from main.logging import logger

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404

from apps.tenants.models import Domain


class TenantMiddleware(object):
    """
        The TenantMiddleware sets the tenant of the request depening on the URL.

        There are 4 types of domains:
        - shared ones (example.com, marketing.example.com, marketingpage.com) - defined in TENANT_DOMAIN and DEFAULT_DOMAINS
        - subdomains of the TENANT_DOMAIN (a.example.com, bar.example.com, foo.example.com) - in the Site model - each tenant has one
        - additional, optional, external domains - they are registered in the Domain model
        - unknown & domains, not linked with any tenant - a 404 is raised for those

        Would be interesting to check out
        - django.contrib.sites CurrentSiteMiddleware
        - https://github.com/bernardopires/django-tenant-schemas


    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        host = request.get_host()

        site_id = None
        request.tenant = None

        # Case 1: An existing site (either belonging to the marketing page itself or a tenant)
        try:
            site = Site.objects.get(domain=host)
            site_id = site.id

            if hasattr(site, 'tenant'):
                request.tenant = site.tenant

        except Site.DoesNotExist:
            pass

        # Case 2 - it is an external domain belonging to a tenant, not registered within the Site model
        try:
            domain = Domain.objects.get(domain=host)
            site_id = domain.tenant.site.id
            request.tenant = domain.tenant
        except Domain.DoesNotExist:
            pass

        logger.debug("TenantMiddleware: Host: {}, Site_ID: {}, Tenant: {}".format(host, site_id, request.tenant))

        domain_parts = host.split('.', 1)

        print(domain_parts)
        print(site_id)

        print(settings.TENANT_SITE_ID)
        print(settings.SITE_ID)

        if site_id:
            settings.SITE_ID = site_id
        else:
            # Case 3 - somebody is accessing a tenant subdomain page, but it does not exist, raise 404

            domain_parts = host.split('.', 1)


            print("YE")


            # Case 2 - this is a sub domain of a tenant
            if (len(domain_parts) == 2 and domain_parts[1] == settings.TENANT_DOMAIN) or \
                    (len(domain_parts) == 1 and domain_parts[0] == settings.TENANT_DOMAIN):
                raise Http404

        response = self.get_response(request)

        return response
