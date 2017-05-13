from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status

from allauth.account.adapter import get_adapter
from allauth.account.views import ConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings

from rest_auth.app_settings import (TokenSerializer,
                                    JWTSerializer,
                                    create_token)
from rest_auth.registration.serializers import (SocialLoginSerializer,
                                                VerifyEmailSerializer)
from rest_auth.views import LoginView
from rest_auth.models import TokenModel
from rest_auth.registration.app_settings import RegisterSerializer
from rest_auth.registration.views import RegisterView

from rest_auth.utils import jwt_encode
from rest_framework import status
from django.http import Http404
from django.contrib.sites.models import Site

from ..models import Tenant
from apps.users.serializers import CreateUserSerializer


class TenantUserRegisterView(RegisterView):

    serializer_class = CreateUserSerializer

    def create(self, request, tenant_name=None, *args, **kwargs):

        tenant_domain = Tenant.objects.get_tenant_domain()

        try:
            site = Site.objects.get(name=f"{tenant_name}.{tenant_domain}")
        except Site.DoesNotExist:
            raise Http404

        if not site.tenant:
            return Response({'error_message': _('There is no tenant for this site.')}, status=status.HTTP_400_BAD_REQUEST)

        tenant = site.tenant

        if not tenant.is_active:
            return Response({'error_message': _('Tenant is deactivated, no registration is possible')}, status=status.HTTP_400_BAD_REQUEST)

        request.data["tenant_name"] = tenant.name

        print("CREATE with tenant_name or not?")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        tenant.add_user(user)

        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)
