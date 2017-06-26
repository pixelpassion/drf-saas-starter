from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.sites.models import Site
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ...users.serializers import CreateUserSerializer
from ..models import Invite, Tenant
from ..serializers import InviteActivationCreateUserSerializer, InviteCreateSerializer, InviteRetrieveSerializer


class TenantRegisterView(RegisterView):
    """Sign up for a tenant, usually for a product or a Software as a area of the web service.

    A company / project name and a sub domain are needed.
    Also the credentials of the first user (the admin) are needed.

    We can overwrite the view because we are using our own Serializer (given with REST_AUTH_REGISTER_SERIALIZERS)
    """
    pass


class TenantUserRegisterView(RegisterView):
    """Sign up for the user of the tenant.

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
            return Response(
                {'error_message': _('There is no tenant for this site.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        tenant = site.tenant

        if not tenant.is_active:
            return Response(
                {'error_message': _('Tenant is deactivated, no registration is possible')},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        tenant.add_user(user)

        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


# FIXME Only a user of the tenant should be able to send invites
# FIXME There should be permissions who is allowed to send invites
class InviteCreateView(CreateAPIView):
    """Invite a person via email to be a user of a tenant."""
    serializer_class = InviteCreateSerializer

    def get_serializer_context(self):
        """Add kwargs to context for the serializer."""
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'kwargs': self.kwargs
        }


class InviteRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Invite.objects.all()
    serializer_class = InviteRetrieveSerializer

    def get(self, request, *args, **kwargs):
        """Add the information when the invite was first clicked and connect existing users to tenant."""
        invite = self.get_object()
        existing_user, invite_used = invite.existing_user_or_invite_used

        if not invite.first_clicked:
            invite.first_clicked = timezone.now()
            invite.save()

        if invite.is_active and existing_user:
            invite.user = invite.existing_user_or_invite_used[0]
            invite.user.is_active = True
            tenant = invite.tenant
            tenant.add_user(invite.user)
            invite.save()
            return Response({'detail': _(f"Your account is now successfully connected to {invite.tenant.name}.")})
        
        return super().get(request, *args, **kwargs)


class InviteActivationView(UpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Invite.objects.all()
    serializer_class = InviteActivationCreateUserSerializer

    def update(self, request, *args, **kwargs):
        """Check the status of the invite and proceed accordingly."""
        invite = self.get_object()
        existing_user, invite_used = invite.existing_user_or_invite_used
        if invite.user:
            return Response({'error': _("The invitation was already used.")},
                            status=status.HTTP_400_BAD_REQUEST)
        elif invite.is_active and not existing_user:
            return super().update(request, *args, **kwargs)
        elif invite.is_active and existing_user:
            return Response({'error': _("You are already a user, please use the link from the email.")},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif not invite.is_active:
            return Response({'error': _("The invitation was not used while it was active.")},
                            status=status.HTTP_401_UNAUTHORIZED)


class GetAllowedVerifyEmailView(VerifyEmailView):
    """Re-enable GET for verifying an email-address.

    rest-auth disabled the GET-method, even though allauth supports it.
    It now doesn't check for CONFIRM_EMAIL_ON_GET.
    """
    allowed_methods = ('GET', 'POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        """Use rest-auth's post, but with kwargs instead of request.data in data."""
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)
