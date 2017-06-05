import factory


class SiteFactory(factory.django.DjangoModelFactory):
    domain = factory.Sequence(lambda n: f'subdomain-{n}.example.com')

    class Meta:
        model = 'sites.Site'
        django_get_or_create = ('domain', )


class TenantFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'tenant-{n}')
    site = factory.SubFactory(SiteFactory)

    class Meta:
        model = 'tenants.Tenant'
