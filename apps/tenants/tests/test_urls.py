from django.test import TestCase
from django.urls import resolve, reverse

from apps.tenants.tests.factories import InviteFactory, TenantFactory


class TestTenantsURLs(TestCase):

    def setUp(self):
        self.tenant = TenantFactory()

    def test_tenants_dashboard_reverse(self):
        assert reverse('tenants:dashboard') == '/tenant/dashboard/'

    def test_tenants_dashboard_resolve(self):
        assert resolve('/tenant/dashboard/').view_name == 'tenants:dashboard'

    def test_tenants_registration_rest_register_reverse(self):
        assert reverse('tenant_rest_register') == '/api/sign-up/tenant/'

    def test_tenants_registration_rest_register_resolve(self):
        assert resolve('/api/sign-up/tenant/').view_name == 'tenant_rest_register'

    def test_tenants_registration_user_rest_register_reverse(self):
        kwargs = {'tenant_name': self.tenant.name}
        assert reverse('user_rest_register', kwargs=kwargs) == f'/api/sign-up/tenant/{self.tenant.name}/user/'

    def test_tenants_registration_user_rest_register_resolve(self):
        assert resolve(f'/api/sign-up/tenant/{self.tenant.name}/user/').view_name == 'user_rest_register'

    def test_tenants_registration_rest_invite_reverse(self):
        kwargs = {'tenant_name': self.tenant.name}
        assert reverse('rest_invite', kwargs=kwargs) == f'/api/sign-up/tenant/{self.tenant.name}/invite/'

    def test_tenants_registration_rest_invite_resolve(self):
        assert resolve(f'/api/sign-up/tenant/{self.tenant.name}/invite/').view_name == 'rest_invite'

    def test_tenants_registration_rest_invite_retrieve_reverse(self):
        invite = InviteFactory()
        assert reverse('rest_invite_retrieve', kwargs={'tenant_name': self.tenant.name, 'pk': invite.pk}) ==\
               f'/api/sign-up/tenant/{self.tenant.name}/invite/{invite.pk}/'

    def test_tenants_registration_rest_invite_retrieve_resolve(self):
        invite = InviteFactory()
        assert resolve(f'/api/sign-up/tenant/{self.tenant.name}/invite/{invite.pk}/').view_name ==\
               'rest_invite_retrieve'

    def test_tenants_registration_rest_invite_activation_reverse(self):
        invite = InviteFactory()
        assert reverse('rest_invite_activation', kwargs={'tenant_name': self.tenant.name, 'pk': invite.pk}) ==\
               f'/api/sign-up/tenant/{self.tenant.name}/invite/{invite.pk}/activate/'

    def test_tenants_registration_rest_invite_activation_resolve(self):
        invite = InviteFactory()
        assert resolve(f'/api/sign-up/tenant/{self.tenant.name}/invite/{invite.pk}/activate/').view_name ==\
               'rest_invite_activation'

    def test_tenants_registration_email_verification_sent_reverse(self):
        assert reverse('account_email_verification_sent') == '/api/sign-up/confirm-email/'

    def test_tenants_registration_email_verification_sent_resolve(self):
        assert resolve('/api/sign-up/confirm-email/').view_name == 'account_email_verification_sent'

    def test_tenants_registration_account_confirm_email_reverse(self):
        pass

    def test_tenants_registration_account_confirm_email_resolve(self):
        pass
