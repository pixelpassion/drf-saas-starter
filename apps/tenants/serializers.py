from rest_framework import serializers

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from apps.users.serializers import CreateUserSerializer

from .models import Tenant


def unique_site_domain(value):

    domain = "{}.{}".format(value, settings.TENANT_DOMAIN)

    try:
        Site.objects.get(domain=domain)
        raise serializers.ValidationError(_('There is already an domain with that name.'))
    except Site.DoesNotExist:
        pass


class TenantSignUpSerializer(serializers.ModelSerializer):
    """
        Serialize data from the tenant (the administration user, who registers for the SaaS.
        A name and domain is used to start an tenant environment. The given user will be the first admin.
    """

    domain = serializers.CharField(label=_(u"Domain"), help_text="The subdomain will be created for the tenant", write_only=True, validators=[unique_site_domain])
    user = CreateUserSerializer(write_only=True)

    class Meta:
        """ """
        model = Tenant
        fields = ('id', 'name', 'domain', 'user')
        extra_kwargs = {'name': {'write_only': True}}

    def create(self, validated_data):
        """call create_tenant on the Tenant model."""

        user_serializer = CreateUserSerializer()
        user = user_serializer.create(validated_data=validated_data.pop('user'))
        Tenant.objects.create_tenant(user=user, **validated_data)

        return user
