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


class InviteFactory(factory.django.DjangoModelFactory):
    tenant = factory.SubFactory(TenantFactory)
    inviter = factory.SubFactory('apps.users.tests.factories.UserFactory')
    email = factory.Sequence(lambda n: 'user-{0}@other-domain.com'.format(n))

    class Meta:
        model = 'tenants.Invite'
