from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from apps.users.serializers import CreateUserSerializer

from ..models import Tenant


class TenantRegisterView(RegisterView):
    """
        Sign up for a tenant, usually for a product or a Software as a area of the web service.
     
        A company / project name and a sub domain are needed.
    
        Also the credentials of the first user (the admin) are needed.
    
        We can overwrite the view because we are using our own Serializer (given with REST_AUTH_REGISTER_SERIALIZERS)
    """

    pass


class TenantUserRegisterView(RegisterView):
    """
    Sign up for the user of the tenant. 
    
    When the tenant is registered and activated, users can register for the tenants space.    
    """

    serializer_class = CreateUserSerializer

    def create(self, request, tenant_name=None, *args, **kwargs):

        tenant_root_domain = Tenant.objects.get_tenant_root_domain()

        try:
            site = Site.objects.get(name=f"{tenant_name}.{tenant_root_domain}")
        except Site.DoesNotExist:
            raise Http404

        if not site.tenant:
            return Response({'error_message': _('There is no tenant for this site.')}, status=status.HTTP_400_BAD_REQUEST)

        tenant = site.tenant

        if not tenant.is_active:
            return Response({'error_message': _('Tenant is deactivated, no registration is possible')}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        tenant.add_user(user)

        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)
