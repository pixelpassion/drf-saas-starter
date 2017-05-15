# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, parsers, renderers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic.base import TemplateView

from apps.api.permissions import IsAuthenticatedOrCreate
from apps.tenants.mixins import TenantAccessRequiredMixin

from .models import User
from .serializers import ChangePasswordSerializer, ResetPasswordSerializer, UserSerializer
from .utils import logout_user


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    """ A view that allows users to login providing their username and password. """

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({'username': user.username })

        return Response({'token': token.key})


class PasswordResetView(APIView):

    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_object(self):
        email = self.request.data.get('email')
        obj = get_object_or_404(self.queryset, email=email)
        return obj

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.send_reset_password_email()
        return Response({}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Password updated successfully."}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(serializer.data['new_password'])
        request.user.save()

        if hasattr(settings,"LOGOUT_ON_PASSWORD_CHANGE") and settings.LOGOUT_ON_PASSWORD_CHANGE:
            logout_user(self.request)

        return Response({"msg": "Password updated successfully."}, status=status.HTTP_200_OK)


