from django.conf import settings
from django.contrib.sites.models import Site
from apps.tenants.models import Domain
from django.http import Http404
from main.logging import logger

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

        # Case 1 - it could be a regular (marketing) domain
        if host in settings.DEFAULT_DOMAINS or host == settings.TENANT_DOMAIN:
            site_id = Site.objects.get(domain=settings.TENANT_DOMAIN).id
            request.tenant = None

        else:
            domain_parts = host.split('.', 1)

            # Case 2 - this is a sub domain of a tenant
            if (len(domain_parts) == 2 and domain_parts[1] == settings.TENANT_DOMAIN) or \
                    (len(domain_parts) == 1 and domain_parts[0] == settings.TENANT_DOMAIN):
                try:
                    site = Site.objects.get(domain=host)
                    site_id = site.id

                    if hasattr(site, 'tenant'):
                        request.tenant = site.tenant
                    else:
                        logger.debug("TenantMiddleware: Host: {}, Site_ID: {} has no tenant!".format(host, site_id))
                        raise Http404

                except Site.DoesNotExist:
                    pass
            # Case 3 - it is an external domain belonging to a tenant
            else:
                try:
                    domain = Domain.objects.get(domain=host)
                    site_id = domain.tenant.site.id
                    request.tenant = domain.tenant
                except Domain.DoesNotExist:
                    pass

        if not site_id:
            logger.warning("TenantMiddleware: Host: {}, no Site found!".format(host))
            raise Http404

        logger.debug("TenantMiddleware: Host: {}, Site_ID: {}, Tenant: {}".format(host, site_id, request.tenant))

        settings.SITE_ID = site_id

        response = self.get_response(request)

        return response

