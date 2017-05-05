from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.views import ConfirmEmailView as AllAuthConfirmEmailView
from main.logging import logger
from rest_auth.app_settings import JWTSerializer, TokenSerializer, create_token
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from apps.api.permissions import IsAuthenticatedOrCreate
from apps.tenants.models import Tenant
from apps.tenants.serializers import TenantSignUpSerializer
from apps.users.utils import send_email_verification

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password')
)


class TenantSignUpView(generics.CreateAPIView):

    queryset = Tenant.objects.all()
    serializer_class = TenantSignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(TenantSignUpView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):

        data = {
            'user': user
        }

        if getattr(settings, 'REST_USE_JWT', False):
            data.update({
                'token': self.token
            })
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = self.get_response_data(user)

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        user = serializer.save()

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        send_email_verification(self.request._request, user, app_settings.EMAIL_VERIFICATION)

        return user
