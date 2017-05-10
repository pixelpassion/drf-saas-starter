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


class UserDetailView(LoginRequiredMixin, TenantAccessRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, TenantAccessRequiredMixin, UpdateView):

    fields = ['first_name', 'last_name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, TenantAccessRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'





class TestView(TemplateView):
    """
    This view should not be included in DRF Docs.
    """
    template_name = "a_test.html"


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



class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    required_scopes = ['special_admin', ]


class UserView(generics.ListAPIView):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    required_scopes = ['special_admin', ]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    An endpoint for users to view and update their profile information.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    #required_scopes = ['special_admin', ]

    def get_object(self):
        return self.request.user


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


# # -*- coding: utf-8 -*-
# from __future__ import absolute_import, unicode_literals
#
# import binascii
# import logging
# import os
#
# import django.contrib.auth.password_validation as validators
# from django.conf import settings
# from django.shortcuts import get_object_or_404
# from django.utils.translation import ugettext as _
# from rest_framework import generics, mixins, status, viewsets
# from rest_framework.permissions import AllowAny
# from rest_framework.renderers import TemplateHTMLRenderer
# from rest_framework.response import Response
# from rest_framework_expiring_authtoken.models import ExpiringToken
#
# from api.mixins import UpdateModelMixin
# from api.permissions import (IsTokenAuthenticatedObjectUser,
#                              IsTokenAuthenticatedRequestUser)
# from authentication.password_validation import UpperLowerSpecialValidator
# from devices.models import Device
# from devices.serializers import DeviceSerializer
# from main.exceptions import *
# from django.conf import settings
# from main.utils import PasswordHistoryCheck
# from .models import User, PasswordHistory
# from .serializers import (BalanceSerializer, ChangePasswordSerializer,
#                           CreateUserSerializer, ActivateUserSerializer,
#                           UserSerializer)
#
# logger = logging.getLogger(__name__)
#
#
# class UserViewSet(mixins.RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
#     """
#     Edit user profile
#
#     retrieve:
#     Get a user profile with means of payments and addresses, using the id (= user_pk)
#     *--
#     JSON response parameters:
#         - id
#         - first_name
#         - last_name
#         - email
#         - mobile-phone
#     *--
#
#     update:
#     Update user profile, using the id (= user_pk)
#     *--
#     JSON response parameters:
#         - id
#         - first_name
#         - last_name
#         - email
#         - mobile-phone
#     *--
#     """
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsTokenAuthenticatedObjectUser,)
#
#
# class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     """
#         The User ViewSet (/users/)
#
#         create: Create a user and send an activation email
#
#     """
#
#     queryset = User.objects.all()
#     serializer_class = CreateUserSerializer
#     authentication_classes = (AllowAny,)
#     permission_classes = (AllowAny,)
#     instance = None
#
#     def create(self, request, *args, **kwargs):
#         """
#         Create a user and send an activation email to the specified email address
#
#         *--
#         JSON response parameters:
#             - user_message_description (hint on how to activate the account)
#         *--
#         """
#         if 'email' not in request.data or 'password' not in request.data:
#             raise EmailAndPasswordNeeded()
#         message_extension = ''
#         if settings.AUTO_ACCOUNT_ACTIVATION == False:
#             activation_token = binascii.hexlify(os.urandom(50)).decode("ascii")
#             request.data["activation_token"] = activation_token
#             message_extension = 'Click on the activation link in your email to activate it.'
#         request.data["is_active"] = settings.AUTO_ACCOUNT_ACTIVATION
#         request.data["email"] = request.data["email"].lower()
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#
#         new_user = {'user_message_description': 'Your account has been successfully created. ' + message_extension}
#
#         # send activation mail
#         if not settings.AUTO_ACCOUNT_ACTIVATION:
#             self.send_activation_mail(self.instance, activation_token)
#
#         return Response(new_user, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         self.instance = serializer.save()
#         self.instance.set_password(serializer.initial_data["password"])
#         self.instance.save()
#         # TODO: 1) should be asynchron, 2) should be created when activated?
#         self.instance.create_contoworks_wallet()
#
#     def send_activation_mail(self, user, activation_token):
#         subject = _(u"Untitled project Account Activation")
#         email_ctx = {
#             'email_verification_url': "%s/api/v1/users/activate_account/%s/" % (settings.BASE_URL, activation_token),
#         }
#         user.send_activation_token('users/email_verification', subject, email_ctx)
#
#
# class ActivationViewSet(viewsets.GenericViewSet, generics.ListAPIView):
#     """
#         Get triggers activation of the user account after signup
#     """
#
#     queryset = User.objects.all()
#     serializer_class = ActivateUserSerializer
#     authentication_classes = (AllowAny,)
#     permission_classes = (AllowAny,)
#     renderer_classes = (TemplateHTMLRenderer,)
#     instance = None
#
#     def list(self, request, activation_token=None, *args, **kwargs):
#         """
#             Get triggers activation of the user account after signup
#
#             *--
#             Response parameters:
#                 - user_message_description (alerted in web view)
#             *--
#         """
#         response_data = {
#             "developer_message": None,
#             "more_info": None,
#         }
#         try:
#             user = User.objects.get(activation_token=activation_token)
#             if user.is_active is True:
#                 response_data["user_message_title"] = _(u"Denied")
#                 response_data["user_message_description"] = _(u"Account already activated")
#             elif len(activation_token) == 100 and user.activation_token == activation_token:
#                 user.is_active = True
#                 user.activation_token = ""
#                 user.save()
#
#                 response_data["user_message_title"] = _(u"Confirm")
#                 response_data["user_message_description"] = _(u"Activation successful")
#         except:
#             response_data["user_message_title"] = _(u"Denied")
#             response_data["user_message_description"] = _(u"Account already activated or activation token not valid")
#
#         return Response({'answer': response_data, 'login_url': settings.WEB_WALLET_BASE_URL}, template_name='registration/activation.html')
#
#     def perform_create(self, serializer):
#         self.instance = serializer.save()
#         self.instance.save()
#
#
# class ChangePasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     """
#         Change a users password
#     """
#
#     queryset = User.objects.all()
#     serializer_class = ChangePasswordSerializer
#     permission_classes = (IsTokenAuthenticatedRequestUser,)
#
#     def create(self, request, user_pk=None, *args, **kwargs):
#         """
#             Change a users password
#
#             * description: a user can change his password from within his own account
#             * requirements: the old password and the email have to be provided again
#             * restrictions: no previously used password can be reused
#
#             *--
#             JSON response parameters:
#                 - user_id
#                 - user_message_title
#                 - user_message_description
#             *--
#         """
#
#         user = User.objects.get(id=user_pk)
#         old_password = request.data.get("old_password")
#         new_password = request.data.get("password")
#
#         if new_password == None or new_password == '':
#             raise NewPasswordNeeded()
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         if old_password == new_password:
#             raise SamePasswords()
#
#         elif user.check_password(old_password) == True:
#             password_history = PasswordHistory.objects.filter(user=user_pk)
#             if PasswordHistoryCheck(new_password, password_history) == True:
#                 # set new password
#                 validators.validate_password(password=new_password, user=user)
#                 UpperLowerSpecialValidator().validate(password=new_password)
#
#                 user.set_password(serializer.initial_data["password"])
#                 user.save()
#                 # save old password in password history
#                 hash_parameters = user.password.split("$")
#                 old_password = PasswordHistory(user=user, salt=hash_parameters[4], password=hash_parameters[5])
#                 old_password.save()
#
#                 response_data = {
#                     'user_id': user.id,
#                     "developer_message": None,
#                     "more_info": None,
#                     "user_message_title": _(u"Confirm"),
#                     "user_message_description": _(u"Password update successful")
#                 }
#
#             else:
#                 raise PasswordAlreadyUsed()
#         else:
#             raise WrongOldPassword()
#
#         return Response(response_data, status=status.HTTP_201_CREATED)
#
#
# class LogoutViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     """
#         The logout viewset
#     """
#
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer
#     permission_classes = (IsTokenAuthenticatedRequestUser,)
#
#     def create(self, request, user_pk=None, device_id=None, *args, **kwargs):
#         """Logout user and deactivate the used device"""
#
#         try:
#             device = Device.objects.get(id=device_id)
#             device.is_active = False
#             device.save()
#         except:
#             raise DeviceDoesNotExist()
#
#         AuthToken = ExpiringToken.objects.get(user=user_pk)
#         AuthToken.delete()
#
#         response_data = {
#             'user_id': user_pk,
#             "developer_message": None,
#             "more_info": None,
#             "user_message_title": _(u"Confirm"),
#             "user_message_description": _(u"Logout successful and device deactivated")
#         }
#
#         return Response(response_data, status=status.HTTP_201_CREATED)


# from django.conf import settings
# from django.utils.decorators import method_decorator
# from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.debug import sensitive_post_parameters
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework.generics import CreateAPIView
# from rest_framework import status
#
# from allauth.account.adapter import get_adapter
# from allauth.account.views import ConfirmEmailView
# from allauth.account.utils import complete_signup
# from allauth.account import app_settings as allauth_settings
#
# from rest_auth.app_settings import (TokenSerializer,
#                                     JWTSerializer,
#                                     create_token)
# from rest_auth.models import TokenModel
# from rest_auth.registration.serializers import (SocialLoginSerializer,
#                                                 VerifyEmailSerializer)
# from rest_auth.utils import jwt_encode
# from rest_auth.views import LoginView
#
# from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes
#
#
# sensitive_post_parameters_m = method_decorator(
#     sensitive_post_parameters('password1', 'password2')
# )
#
#
# class UserRegisterView(CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = register_permission_classes()
#     token_model = TokenModel
#
#     @sensitive_post_parameters_m
#     def dispatch(self, *args, **kwargs):
#         return super(RegisterView, self).dispatch(*args, **kwargs)
#
#     def get_response_data(self, user):
#         if allauth_settings.EMAIL_VERIFICATION == \
#                 allauth_settings.EmailVerificationMethod.MANDATORY:
#             return {"detail": _("Verification e-mail sent.")}
#
#         if getattr(settings, 'REST_USE_JWT', False):
#             data = {
#                 'user': user,
#                 'token': self.token
#             }
#             return JWTSerializer(data).data
#         else:
#             return TokenSerializer(user.auth_token).data
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#
#         return Response(self.get_response_data(user),
#                         status=status.HTTP_201_CREATED,
#                         headers=headers)
#
#     def perform_create(self, serializer):
#         user = serializer.save(self.request)
#         if getattr(settings, 'REST_USE_JWT', False):
#             self.token = jwt_encode(user)
#         else:
#             create_token(self.token_model, user, serializer)
#
#         complete_signup(self.request._request, user,
#                         allauth_settings.EMAIL_VERIFICATION,
#                         None)

