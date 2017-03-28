from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from apps.users.serializers import CreateUserSerializer
from .models import Tenant
from rest_framework.validators import UniqueValidator
from django.contrib.sites.models import Site
from django.conf import settings
from django.db import transaction
from main.logging import logger

def unique_site_domain(value):

    domain = "{}.{}".format(value, settings.TENANT_DOMAIN)

    try:
        Site.objects.get(domain=domain)
        raise serializers.ValidationError(_('There is already an domain with that name.'))
    except Site.DoesNotExist:
        pass


class TenantSerializer(serializers.ModelSerializer):
    """Serialize data from the User """

    domain = serializers.CharField(label=_(u"Domain"), help_text="The domain name of the tenant", write_only=True, validators=[unique_site_domain])

    class Meta:
        """ """
        model = Tenant
        fields = ('id', 'name', 'domain', 'is_active', )
        read_only_fields = ('is_active', )

    # def create(self, validated_data):
    #     """call create_tenant on the Tenant model."""
    #
    #     logger.warning(validated_data)
    #
    #     user_serializer = CreateUserSerializer()
    #     user = user_serializer.create(validated_data=validated_data["user"])
    #     del(validated_data['user'])
    #
    #     tenant = Tenant.objects.create_tenant(**validated_data)
    #
    #     return tenant


class TenantSignUpSerializer(serializers.ModelSerializer):
    """Serialize data from the User """

    domain = serializers.CharField(label=_(u"Domain"), help_text="Domain of the tenant", write_only=True, validators=[unique_site_domain])

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

