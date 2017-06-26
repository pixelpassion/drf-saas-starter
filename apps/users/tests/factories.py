import factory
from allauth.account.models import EmailAddress

from apps.tenants.tests.factories import TenantFactory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )


class VerifiedUserFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    email = factory.LazyAttribute(lambda a: a.user.email)
    verified = True

    class Meta:
        model = EmailAddress


class UserTenantRelationshipFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    tenant = factory.SubFactory(TenantFactory)

    class Meta:
        model = 'users.UserTenantRelationship'
